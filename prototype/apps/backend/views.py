import os
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import PersonPermissions, CandidateSkillPermissions, CandidateDocPermissions, JobPostPermissions, JobSkillPermissions
from .matcher import FindCandidatesForJob, CreateManualJobMatch

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'admins': reverse('admins-list', request=request, format=format),
        'candidates': reverse('candidates-list', request=request, format=format),
        'candidate-skills': reverse('candidate-skills-list', request=request, format=format),
        'employers': reverse('employers-list', request=request, format=format),
        'recruiters': reverse('recruiters-list', request=request, format=format),
        'skills': reverse('skill-list', request=request, format=format),
        'job-posts': reverse('job-post-list', request=request, format=format),
        'job-skills': reverse('job-skill-list', request=request, format=format),
        'job-matches': reverse('job-match-list', request=request, format=format),
        'favourites-candidates': reverse('favourites-candidates-list', request=request, format=format),
        'favourites-jobs': reverse('favourites-jobs-list', request=request, format=format)
    })

def GetUserRole(user):
    if user.role == 'C':
        return Candidate.objects.get(pk=user.id)
    elif user.role == 'E':
        return Employer.objects.get(pk=user.id)
    elif user.role == 'R':
        return Recruiter.objects.get(pk=user.id)
    else:
        raise ValidationError('Invalid user role: ' + user.role)

class CandidateViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = (permissions.IsAuthenticated, PersonPermissions)

    # This function can optionally filter candidates by city and skills.
    # It will return candidates in any of the specified cities who possess all
    # the specified skills. If no cities or skills are specified it will
    # return all Candidates.

    def get_queryset(self):
        params = self.request.query_params
        skills = params.get('skills', None)
        cities = params.get('cities', None)
        if cities is not None:
            cities = set([ s.strip() for s in cities.split(',') ])
        first_name = params.get('first_name', None)
        last_name = params.get('last_name', None)
        email = params.get('email', None)
        if email is not None:
            email = email.lower()
        gender = params.get('gender', None)
        highest_education = params.get('highest_education', None)
        if skills is not None:
            # For each skill, construct a set of the candidates who possess the skill.
            candidate_sets = []
            for skill in skills.split(','):
                query = CandidateSkill.objects.filter(skill=skill)
                # Possibly filter the candidates by other fields.
                if first_name is not None:
                    query = query.filter(candidate__user__first_name__iexact=first_name)
                if last_name is not None:
                    query = query.filter(candidate__user__last_name__iexact=last_name)
                if cities is not None:
                    query = query.filter(candidate__user__city__in=cities)
                if email is not None:
                    query = query.filter(candidate__user__email=email)
                if gender is not None:
                    query = query.filter(candidate__gender=gender)
                if highest_education is not None:
                    query = query.filter(candidate__highest_education__gte=highest_education)
                candidate_sets.append({ cs.candidate for cs in query })
            # The intersection of all the sets will be the candidates who possess all the skills.
            return set.intersection(*candidate_sets)
        else:
            # Optionally filter the candiates by city, first name, and last name.
            if cities is not None:
                query = Candidate.objects.filter(user__city__in=cities)
            else:
                query = Candidate.objects.all()
            if first_name is not None:
                query = query.filter(user__first_name__iexact=first_name)
            if last_name is not None:
                query = query.filter(user__last_name__iexact=last_name)
            if email is not None:
                query = query.filter(user__email=email)
            if gender is not None:
                query = query.filter(gender=gender)
            if highest_education is not None:
                query = query.filter(highest_education__gte=highest_education)
            return query

class CandidateSkillViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CandidateSkill.objects.all()
    permission_classes = (permissions.IsAuthenticated, CandidateSkillPermissions)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return CandidateSkillOutboundSerializer
        return CandidateSkillInboundSerializer

    def get_queryset(self):
        candidate = self.request.query_params.get('candidate', None)
        if candidate is not None:
            return CandidateSkill.objects.filter(candidate=candidate).order_by('skill__name')
        else:
            return CandidateSkill.objects.all()

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated, CandidateDocPermissions)

    def get_queryset(self):
        candidate = self.request.query_params.get('candidate', None)
        if candidate is not None:
            return Document.objects.filter(candidate=candidate).order_by('description')
        else:
            return Document.objects.all()

    def destroy(self, request, *args, **kwargs):
        doc = Document.objects.get(pk=kwargs['pk'])
        # Remove the file associated with this Document.
        file_path = os.path.join('user_files', str(request.user.id), doc.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return super(DocumentViewSet, self).destroy(request, *args, **kwargs)

class EmployerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (permissions.IsAuthenticated, PersonPermissions)

class RecruiterViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer
    permission_classes = (permissions.IsAuthenticated, PersonPermissions)

class SkillViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            if str.isnumeric(category):
                query_set = Skill.objects.filter(category=category)
            elif category == 'root':
                query_set = Skill.objects.filter(category=None)
            else:
                query_set = Skill.objects.filter(category__name=category)
        else:
            query_set = Skill.objects.all()
        return query_set.order_by('name')

class JobPostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = (permissions.IsAuthenticated, JobPostPermissions)

    def get_queryset(self):
        params = self.request.query_params
        skills = params.get('skills', None)
        cities = params.get('cities', None)
        if cities is not None:
            cities = set([ s.strip() for s in cities.split(',') ])
        name_contains = params.get('name_contains', None)
        desc_contains = params.get('desc_contains', None)
        min_education = params.get('min_education', None)
        max_education = params.get('max_education', None)
        contact_person = params.get('contact_person', None)
        min_salary = params.get('min_salary', None)
        max_salary = params.get('max_salary', None)
        states = params.get('states', None)
        if states is not None:
            states = set([ s.strip() for s in states.split(',') ])
        if skills is not None:
            # For each skill, construct a set of the jobs that require the skill.
            job_sets = []
            for skill in skills.split(','):
                query = JobSkill.objects.filter(skill=skill)
                # Possibly filter the jobs by other fields.
                if cities is not None:
                    query = query.filter(job__city__in=cities)
                if name_contains is not None:
                    query = query.filter(job__name__icontains=name_contains)
                if desc_contains is not None:
                    query = query.filter(job__description__icontains=desc_contains)
                # Filter jobs by education requirement.
                if min_education is not None:
                    query = query.filter(job__required_education__gte=min_education)
                if max_education is not None:
                    query = query.filter(job__required_education__lte=max_education)
                if contact_person is not None:
                    query = query.filter(job__contact_person=contact_person)
                if min_salary is not None:
                    query = query.filter(job__equiv_annual_salary__gte=min_salary)
                if max_salary is not None:
                    query = query.filter(job__equiv_annual_salary__lte=max_salary)
                if states is not None:
                    query = query.filter(job__state__in=states)
                job_sets.append({ js.job for js in query })
            # The intersection of all the sets will be the candidates who possess all the skills.
            return set.intersection(*job_sets)

        if cities is not None:
            query = JobPost.objects.filter(city__in=cities)
        else:
            query = JobPost.objects.all()
        if name_contains is not None:
            query = query.filter(name__icontains=name_contains)
        if desc_contains is not None:
            query = query.filter(description__icontains=desc_contains)
        # Filter jobs by education requirement.
        if min_education is not None:
            query = query.filter(required_education__gte=min_education)
        if max_education is not None:
            query = query.filter(required_education__lte=max_education)
        if contact_person is not None:
            query = query.filter(contact_person=contact_person)
        if min_salary is not None:
            query = query.filter(equiv_annual_salary__gte=min_salary)
        if max_salary is not None:
            query = query.filter(equiv_annual_salary__lte=max_salary)
        if states is not None:
            query = query.filter(state__in=states)
        return query

    def destroy(self, request, *args, **kwargs):
        job = JobPost.objects.get(pk=kwargs['pk'])
        matches = JobMatch.objects.filter(job=job)
        if len(matches) > 0:
            return Response('You cannot delete a job after matches have been created. Please withdraw the job instead.', status=400)
        job.delete()
        return Response(status=204)

    @action(methods=['post'], detail=True)
    def withdraw_job(self, request, pk):
        job = JobPost.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user != job.contact_person.user:
            return Response('Only the employer can withdraw a job.', status=403)
        if job.state == 'F':
            return Response('You cannot withdraw a job after somebody has been hired.', status=400)
        job.state = 'W'
        job.save()
        # Update the state of any JobMatches for this JobPost.
        matches = JobMatch.objects.filter(job=job).exclude(state__in=['DC', 'DE', 'JD'])
        for om in matches:
            om.state = 'W'
            om.save()
        return Response(JobPostSerializer(job).data, status=200)

class JobPostAndSkillsViewSet(JobPostViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobPost.objects.all()
    serializer_class = JobPostAndSkillSerializer
    permission_classes = (permissions.IsAuthenticated, JobPostPermissions)

class JobSkillViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobSkill.objects.all()
    permission_classes = (permissions.IsAuthenticated, JobSkillPermissions)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return JobSkillOutboundSerializer
        return JobSkillInboundSerializer

    def get_queryset(self):
        jobid = self.request.query_params.get('job', None)
        if jobid is not None:
            return JobSkill.objects.filter(job=jobid)
        else:
            return JobSkill.objects.all()

class JobMatchViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobMatch.objects.all()
    serializer_class = JobMatchSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        role = self.request.user.role
        user_id = self.request.user.id
        print(role, user_id)
        if role == 'C':
            # Candidates can only see matches for themselves.
            query = JobMatch.objects.filter(candidate=user_id)
        elif role == 'E':
            # Employers can only see matches for their jobs.
            query = JobMatch.objects.filter(job__contact_person=user_id)
        else:
            # Recruiters can only see matches that they created.
            query = JobMatch.objects.filter(created_by=user_id)
        # Support additional filtering by job or state.
        params = self.request.query_params
        jobid = params.get('job', None)
        if jobid is not None:
            query = query.filter(job=jobid)
        states = params.get('states', None)
        if states is not None:
            query = query.filter(state__in=states.split(','))
        return query

    def delete(self, request):
        params = self.request.query_params
        job = params.get('job', None)
        candidate = params.get('candidate', None)
        JobMatch.objects.filter(candidate=candidate, job=job).delete()
        return Response(status=204)

    @action(methods=['post'], detail=True)
    def decline(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if match.state not in {'DC', 'DE', 'JO', 'H', 'JD', 'F', 'W'}:
            if user == match.candidate.user:
                match.state = 'DC'
                match.save()
            elif user == match.job.contact_person.user:
                match.state = 'DE'
                match.save()
            else:
                return Response('Only the employer or candidate can decline a job match.', status=403)
        else:
            return Response('The job match cannot be declined in its current state.', status=400)
        return Response(JobMatchSerializer(match).data, status=200)

    @action(methods=['post'], detail=True)
    def express_interest(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user == match.candidate.user:
            if match.state not in {'CI', 'DE', 'P', 'JO', 'H', 'F', 'W'}:
                if match.state == 'EI':
                    # Candidate & Employer have both indicated interest.
                    match.state = 'P'
                else:
                    match.state = 'CI'
                match.save()
        elif user == match.job.contact_person.user:
            if match.state not in {'EI', 'DC', 'P', 'JO', 'H', 'JD', 'F', 'W'}:
                if match.state == 'CI':
                    # Candidate & Employer have both indicated interest.
                    match.state = 'P'
                else:
                    match.state = 'EI'
                match.save()
        else:
            return Response('Only the employer or candidate can accept a job match.', status=403)
        return Response(JobMatchSerializer(match).data, status=200)

    @action(methods=['post'], detail=True)
    def make_job_offer(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user != match.job.contact_person.user:
            return Response('Only the employer can make a job offer.', status=403)
        if match.state != 'P':
            return Response('You can only offer a job if the state is "In Progress".', status=404)
        # Record the fact that an offer has been made.
        match.state = 'JO'
        match.job.state = 'JO'
        match.save()
        match.job.save()
        return Response(JobMatchSerializer(match).data, status=200)

    @action(methods=['post'], detail=True)
    def withdraw_job_offer(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user != match.job.contact_person.user:
            return Response('Only the employer can withdraw a job offer.', status=403)
        if match.state != 'JO':
            return Response('There is no job offer to withdraw.', status=404)
        # Return the state to "In Progress". From here the employer can decline the match
        # altogether, or continue negotiations with the candidate and perhaps make another
        # offer in the future.
        match.state = 'P'
        match.job.state = 'L'
        match.save()
        match.job.save()
        return Response(JobMatchSerializer(match).data, status=200)

    @action(methods=['post'], detail=True)
    def accept_job_offer(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user != match.candidate.user:
            return Response('Only the candidate can accept a job offer.', status=403)
        if match.state != 'JO':
            return Response('There is no job offer to decline.', status=404)
        job = match.job
        match.state = 'H'
        # Record the hire in the job object.
        job.state = 'F'
        job.hired_person = match.candidate
        # Candidate is no longer looking for work.
        match.candidate.looking_for_work = False
        match.save()
        job.save()
        match.candidate.save()
        # Update the states of any other JobMatches for this JobPost.
        other_matches = JobMatch.objects.filter(job=job).exclude(state__in=['DC', 'DE'], candidate=match.candidate)
        for om in other_matches:
            if om.state in {'N', 'CI', 'EI', 'P', 'JO'}:
                om.state = 'F'
                om.save()
        return Response(JobMatchSerializer(match).data, status=200)

    @action(methods=['post'], detail=True)
    def decline_job_offer(self, request, pk):
        match = JobMatch.objects.get(pk=pk)
        user = SSUser.objects.get(pk=request.user.id)
        if user != match.candidate.user:
            return Response('Only the candidate can decline a job offer.', status=403)
        if match.state != 'JO':
            return Response('There is no job offer to decline.', status=404)
        # Update the state of the JobMatch and the associated JobPost.
        match.state = 'JD'
        match.job.state = 'L'
        match.save()
        match.job.save()
        return Response(JobMatchSerializer(match).data, status=200)

class JobMatchAndCandidateViewSet(JobMatchViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobMatch.objects.all()
    serializer_class = JobMatchAndCandidateSerializer
    permission_classes = (permissions.IsAuthenticated,)

class JobMatchAndPostViewSet(JobMatchViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = JobMatch.objects.all()
    serializer_class = JobMatchAndPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

# Limit the users to 100 MB of documents.
USER_FILE_UPLOAD_LIMIT=100
USER_FILE_UPLOAD_LIMIT_BYTES = USER_FILE_UPLOAD_LIMIT * 1024 * 1024

def SaveUserFile(request, filename, old_filename):
    downloaded_file = request.data['file']
    # Save each user's files in a different directory. Use the user ID
    # as the directory name because it is guaranteed to be unique.
    save_dir = os.path.join('user_files', str(request.user.id))
    total_size = 0
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        total_size = os.path.getsize(save_dir)
        # Subtract the size of the file that we're going to replace, if any.
        if old_filename != '':
            old_path = os.path.join(save_dir, old_filename)
            if os.path.exists(old_path):
                total_size -= os.path.getsize(old_path)
    total_size += downloaded_file.size
    if total_size > USER_FILE_UPLOAD_LIMIT_BYTES:
        return False
    # Save the file to disk
    with open(os.path.join(save_dir, filename), 'wb') as save_file:
        for chunk in downloaded_file.chunks():
            save_file.write(chunk)
    return True

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):
        # Verify that the user is a Candidate before saving the file.
        candidate = Candidate.objects.get(pk=request.user.id)
        if not SaveUserFile(request, filename, filename):
            return Response('Uploading this file would exceed your total storage limit of {:,} megabytes.'.format(
                USER_FILE_UPLOAD_LIMIT), status=400)
        # Create document record.
        c_doc, created = Document.objects.update_or_create(
            candidate=candidate, filename=filename,
            defaults={
                'type': request.data['type'],
                'description': request.data['description']
            })
        return Response(DocumentSerializer(c_doc).data, status=201)

    def delete(self, request, filename, format=None):
        file_path = os.path.join('user_files', str(request.user.id), filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            status = 204
        else:
            status = 404
        # Delete document record.
        Document.objects.filter(candidate=request.user.id, filename=filename).delete()
        return Response(status=status)

class PhotoUploadView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):
        if request.data['file'].size > 524288:
            return Response('Photo exceeds the size limit of 512 KB.', status=400)
        role = GetUserRole(request.user)
        if not SaveUserFile(request, filename, role.photo):
            return Response('Uploading this file would exceed your total storage limit of {:,} megabytes.'.format(
                USER_FILE_UPLOAD_LIMIT), status=400)
        # Delete the previous profile photo, if any.
        if role.photo != filename:
            if role.photo != '':
                old_path = os.path.join('user_files', str(request.user.id), role.photo)
                if os.path.exists(old_path):
                    os.remove(old_path)
            role.photo = filename
            role.save()
        return Response(status=204)

    def delete(self, request, filename, format=None):
        file_path = os.path.join('user_files', str(request.user.id), filename)
        if not os.path.exists(file_path):
            return Response(status=404)
        os.remove(file_path)
        # The user now has no profile photo.
        role = GetUserRole(request.user)
        role.photo = ''
        role.save()
        return Response(status=204)

class FileListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user, format=None):
        user_dir = os.path.join('user_files', user)
        if not os.path.exists(user_dir):
            return Response([], status=200)
        return Response(os.listdir(user_dir), status=200)

class BinaryRenderer(BaseRenderer):
    media_type = 'application/*'
    format = 'binary'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class FileDownloadView(APIView):
    renderer_classes = (BinaryRenderer, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, user, filename, format=None):
        file_path = os.path.join('user_files', user, filename)
        if not os.path.exists(file_path):
            return Response(status=404)
        with open(file_path, 'rb') as data_file:
            data = data_file.read()
        return Response(data, status=200)

class AutoMatchView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        max_candidates = int(request.data.get('max_candidates', 10))
        jobpost = JobPost.objects.get(pk=request.data.get('job'))
        success, result = FindCandidatesForJob(jobpost, max_candidates)
        if success:
            return Response(JobMatchSerializer(result, many=True).data, status=200)
        # If success is False, 'result' will be an error message string.
        return Response(result, status=400)

class ManualMatchView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        jobpost = JobPost.objects.get(pk=request.data.get('job'))
        candidate = Candidate.objects.get(pk=request.data.get('candidate'))
        # Employers can only create job matches for their own jobs.
        # Candidates can only create job matches with themselves as the candidate.
        # Recruiters can creator matches for any job or candidate.
        creator = request.user
        # Make sure nobody does anything that they shouldn't.
        if creator.role == 'C':
            if creator != candidate.user:
                return Response("You can only request job matches for yourself.", status=400)
        elif creator.role == 'E' and creator != jobpost.contact_person.user:
            return Response("You can only match candidates to your own jobs.", status=400)
        # Now try to create a JobMatch. If validate is True, this will fail if the
        # Candidate does not meet the job requirements.
        success, result = CreateManualJobMatch(jobpost, candidate, creator,
            request.data.get('validate', True))
        if success:
            return Response(JobMatchAndPostSerializer(result).data, status=200)
        # If success is False, 'result' will be an error message string.
        return Response(result, status=400)

class FavouritesCandidatesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = FavouritesCandidates.objects.all()
    serializer_class = FavouritesCandidatesSerializer
    permission_classes = (permissions.IsAuthenticated, PersonPermissions)

    def delete(self, request):
        params = self.request.query_params
        SSUser = params.get('SSUser', None)
        candidate = params.get('candidate', None)
        FavouritesCandidates.objects.filter(candidate=candidate, SSUser=SSUser).delete()
        return Response(status=204)

    def get_queryset(self):
        params = self.request.query_params
        currentuser = params.get('SSUser', None)
        if currentuser is not None:
            query = FavouritesCandidates.objects.filter(SSUser=currentuser)
        else:
            query = FavouritesCandidates.objects.all()
              
        return query

class FavouritesJobsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = FavouritesJobs.objects.all()
    permission_classes = (permissions.IsAuthenticated, PersonPermissions)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return FavouritesJobsOutboundSerializer
        return FavouritesJobsInboundSerializer

    def delete(self, request):
        params = self.request.query_params
        SSUser = params.get('SSUser', None)
        job = params.get('job', None)
        FavouritesJobs.objects.filter(job=job, SSUser=SSUser).delete()
        return Response(status=204)

    def get_queryset(self):
        params = self.request.query_params
        currentuser = params.get('SSUser', None)
        if currentuser is not None:
            query = FavouritesJobs.objects.filter(SSUser=currentuser)
        else:
            query = FavouritesJobs.objects.all()
              
        return query