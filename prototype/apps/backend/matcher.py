from django.core.exceptions import ValidationError
from .models import Candidate, CandidateSkill, JobPost, JobSkill, JobMatch

def CreateManualJobMatch(jobpost, candidate, creator, validate):
    if len(JobMatch.objects.filter(job=jobpost, candidate=candidate)) > 0:
        return False, 'Candidate has already been matched to "{}".'.format(jobpost.name)
    job_skills = JobSkill.objects.filter(job=jobpost)
    skill_priorities = { js.skill : js.priority for js in job_skills }
    # Only load skills which are relevant to the job.
    candidate_skills = { cs.skill: cs for cs in CandidateSkill.objects.filter(candidate=candidate, skill__in=skill_priorities) }
    if validate:
        if not candidate.looking_for_work:
            return False, 'Candidate is not looking for work.'
        if candidate.highest_education < jobpost.required_education:
            return False, 'Candidate does not have the necessary education for this job.'
        if candidate.minimum_salary > jobpost.equiv_annual_salary:
            return False, 'Salary is below the candidate\'s minimum salary expectation.'
        essential_skills = [ js for js in job_skills if js.priority == 5 ]
        for js in essential_skills:
            if not js.skill in candidate_skills:
                return False, 'Candidate does not possess the skill {}, which is essential for this job.'.format(js.skill.name)
            cs = candidate_skills[js.skill]
            if cs.months_experience < js.months_experience:
                return False, 'Candidate does not have enough experience at {}.'.format(js.skill.name)
            if cs.proficiency < js.proficiency:
                return False, 'Candidate does not have the required proficiency at {}.'.format(js.skill.name)
    # Calculate the candidate's score for this job based on their proficiency at the skills in the job post.
    # Scores can be used to compare the suitability of different candidates for a given job. However, it is
    # not generally meaningful to compare the scores for different jobs.
    score = 0
    for cs in candidate_skills.values():
        score += cs.proficiency * skill_priorities[cs.skill]
    # Create a JobMatch object, or update the score if a JobMatch already exists.
    match = JobMatch.objects.create(job=jobpost, candidate=candidate, created_by=creator, score=score)
    return True, match

def FindCandidatesForJob(jobpost, max_candidates=10):
    if jobpost.state in {'F', 'W'}:
        return False, 'You cannot find candidates for a filled or withdrawn job post.'
    job_skills = JobSkill.objects.filter(job=jobpost)
    essential_skills = [ js for js in job_skills if js.priority == 5 ]
    if len(essential_skills) == 0:
        return False, 'You must specify at least one essential skill for the job before you can find candidates.'
    # Put any existing matches for this JobPost into a dictionary with the candidate as the key.
    old_matches = { m.candidate : m for m in JobMatch.objects.filter(job=jobpost) }
    candidate_sets = []
    # For each essential skill, create a set of candidates in the specified city who posses the skill,
    # and also meet the minimum education requirement.
    for js in essential_skills:
        skill_query = CandidateSkill.objects.filter(skill=js.skill, proficiency__gte=js.proficiency, candidate__user__city=jobpost.city,
            candidate__looking_for_work=True, candidate__minimum_salary__lte=jobpost.equiv_annual_salary)
        if js.months_experience > 0:
            skill_query = skill_query.filter(months_experience__gte=js.months_experience)
        if jobpost.required_education > 0:
            skill_query = skill_query.filter(candidate__highest_education__gte=jobpost.required_education)
        candidate_set = { cs.candidate for cs in skill_query }
        # If no candidates have one of the essential skills then we can give up now.
        if len(candidate_set) == 0:
            return True, []
        candidate_sets.append(candidate_set)
    # The intersection of all the sets will be the candidates who possess all the skills.
    candidates = set.intersection(*candidate_sets)
    matches = []
    if len(candidates) > 0:
        candidate_scores = []
        skill_priorities = { js.skill : js.priority for js in job_skills }
        # Now score each candidate.
        for candidate in candidates:
            # Assign each candidate a score based on their proficiency at the skills in the job post.
            score = 0
            for cs in CandidateSkill.objects.filter(candidate=candidate, skill__in=skill_priorities):
                score += cs.proficiency * skill_priorities[cs.skill]
            candidate_scores.append((score, candidate))
        # Sort the matches in descending order of candidate score.
        candidate_scores.sort(key=lambda pair: pair[0], reverse=True)
        # Create JobMatch objects for the remaining candidates.
        for score, candidate in candidate_scores:
            match = old_matches.pop(candidate, None)
            if match is None:
                matches.append(JobMatch.objects.create(job=jobpost, candidate=candidate, score=score, state='N'))
            else:
                # We may as well update the scores even for inactive matches,
                # since the candidate and/or employer can change their minds
                # and make the match active again.
                if match.score != score:
                    match.score = score
                    match.save()
                if match.IsActive():
                    matches.append(match)
            # Stop after we have the required number of active matches.
            if len(matches) >= max_candidates:
                break
    # Any matches left in old_matches no longer make the cut for this job.
    # This could happen because the job requirements have been increased, more suitable
    # candidates have appeared, or the candidate has downgraded their skills.
    for old_match in old_matches.values():
        # Only delete if no action has been taken on the match.
        if old_match.state == 'N':
            old_match.delete()
    return True, matches
