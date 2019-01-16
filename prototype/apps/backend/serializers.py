from datetime import date
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSUser
        fields = ('id', 'role', 'first_name', 'last_name', 'email', 'phone', 'city', 'date_joined')
        read_only_fields = ('role', 'date_joined',)

        # We need to remove the UniqueValidator on email because it doesn't
        # work properly with nested serializers.
        extra_kwargs = {
            'email': {
                'validators': [],
            }
        }

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Admin
        fields = ('user')
        depth = 1

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        admin, created = Admin.objects.update_or_create(user=user)
        return admin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user.email = user_data.pop('email').lower()
        instance.user.first_name = user_data.pop('first_name')
        instance.user.last_name = user_data.pop('last_name')
        instance.user.city = user_data.pop('city')
        instance.user.save()
        return instance

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Candidate
        fields = ('user', 'date_of_birth', 'gender', 'highest_education', 'looking_for_work', 'minimum_salary', 'photo')
        read_only_fields = ('photo',)

    def create(self, validated_data):
        raise ValidationError('Candidates can only be created via registration.')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user.email = user_data.pop('email').lower()
        instance.user.phone = user_data.pop('phone')
        instance.user.first_name = user_data.pop('first_name')
        instance.user.last_name = user_data.pop('last_name')
        instance.user.city = user_data.pop('city')
        instance.user.save()
        instance.date_of_birth = validated_data.pop('date_of_birth')
        instance.gender = validated_data.pop('gender')
        instance.highest_education = validated_data.pop('highest_education')
        instance.looking_for_work = validated_data.pop('looking_for_work')
        instance.minimum_salary = validated_data.pop('minimum_salary')
        instance.save()
        return instance

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Skill
        fields = ('id', 'category', 'name', 'description', 'type')

    def validate_category(self, value):
        if value is not None and value.type == 'L':
            raise ValidationError(value.name + ' is not a valid category.')
        return value

class CandidateSkillOutboundSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = CandidateSkill
        fields = ('id', 'skill', 'candidate', 'proficiency', 'months_experience', 'evidence', 'experience', 'experience_unit')
        read_only_fields = ('candidate', 'experience', 'experience_unit')

class CandidateSkillInboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkill
        fields = ('id', 'skill', 'candidate', 'proficiency', 'months_experience', 'evidence', 'experience', 'experience_unit')
        read_only_fields = ('candidate', 'experience', 'experience_unit')

    def create(self, validated_data):
        # Candidates use the user as the primary key.
        candidate = Candidate.objects.get(pk=self.context['request'].user)
        c_skill, created = CandidateSkill.objects.update_or_create(
            candidate=candidate, skill=validated_data.pop('skill'),
            defaults={
                'proficiency': validated_data.pop('proficiency'),
                'months_experience': validated_data.pop('months_experience')
            })
        c_skill.evidence.set(validated_data.pop('evidence'))
        return c_skill

    def validate_skill(self, value):
        if value.type != 'L':
            raise ValidationError('Skill cannot be a category.')
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'candidate', 'filename', 'type', 'description', 'date_uploaded')
        read_only_fields = ('id', 'candidate', 'filename', 'date_uploaded')

    def create(self, validated_data):
        raise ValidationError('Document records can only be created via the upload API.')

class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Employer
        fields = ('user', 'company', 'website', 'photo')
        read_only_fields = ('photo', )
        depth = 1

    def create(self, validated_data):
        raise ValidationError('Employers can only be created via registration.')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user.email = user_data.pop('email').lower()
        instance.user.phone = user_data.pop('phone')
        instance.user.first_name = user_data.pop('first_name')
        instance.user.last_name = user_data.pop('last_name')
        instance.user.city = user_data.pop('city')
        instance.user.save()
        instance.company = validated_data.pop('company')
        instance.website = validated_data.pop('website')
        instance.save()
        return instance

class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Recruiter
        fields = ('user', 'company', 'website', 'photo')
        read_only_fields = ('photo', )
        depth = 1

    def create(self, validated_data):
        raise ValidationError('Recruiters can only be created via registration.')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user.email = user_data.pop('email').lower()
        instance.user.phone = user_data.pop('phone')
        instance.user.first_name = user_data.pop('first_name')
        instance.user.last_name = user_data.pop('last_name')
        instance.user.city = user_data.pop('city')
        instance.user.save()
        instance.company = validated_data.pop('company')
        instance.website = validated_data.pop('website')
        instance.save()
        return instance

class JobPostSerializer(serializers.ModelSerializer):
    contact_person = EmployerSerializer(read_only=True)

    class Meta:
        model = JobPost
        fields = ('id', 'name', 'description', 'city', 'required_education', 'skills', 'contact_person', 'pay_type', 'pay', 'equiv_annual_salary', 'date_posted', 'state', 'hired_person')
        read_only_fields = ('contact_person', 'equiv_annual_salary', 'date_posted', 'skills', 'state', 'hired_person')

    def create(self, validated_data):
        # Look up the Employer from the user associated with the request.
        employer = Employer.objects.get(pk=self.context['request'].user)
        pay_type = validated_data.pop('pay_type')
        pay = validated_data.pop('pay')
        job_post = JobPost.objects.create(
            name=validated_data.pop('name'),
            description=validated_data.pop('description'),
            city=validated_data.pop('city'),
            required_education=validated_data.pop('required_education'),
            contact_person=employer,
            pay_type=pay_type,
            pay=pay,
            equiv_annual_salary=pay)
        return job_post

    def update(self, instance, validated_data):
        instance.name = validated_data.pop('name')
        instance.description = validated_data.pop('description')
        instance.city = validated_data.pop('city')
        instance.required_education = validated_data.pop('required_education')
        instance.pay_type = validated_data.pop('pay_type')
        instance.pay = validated_data.pop('pay')
        instance.equiv_annual_salary = JobPost.EquivalentAnnualSalary(instance.pay_type, instance.pay)
        instance.save()
        return instance

# Serialize JobPost without skills or contact person.

class BasicJobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ('id', 'name', 'description', 'city', 'required_education', 'pay_type', 'pay', 'equiv_annual_salary', 'date_posted', 'state', 'hired_person')
        read_only_fields = ('equiv_annual_salary', 'date_posted', 'state', 'hired_person')

class JobSkillOutboundSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = JobSkill
        fields = ('id', 'job', 'skill', 'priority', 'proficiency', 'months_experience', 'experience', 'experience_unit')

class JobSkillInboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ('id', 'job', 'skill', 'priority', 'proficiency', 'months_experience')

    def create(self, validated_data):
        job = validated_data.pop('job')
        if job.contact_person.user != self.context['request'].user:
            raise PermissionDenied
        job_skill, created = JobSkill.objects.update_or_create(
            job=job,
            skill=validated_data.pop('skill'),
            priority=validated_data.pop('priority'),
            proficiency=validated_data.pop('proficiency'),
            months_experience=validated_data.pop('months_experience'))
        return job_skill

class JobPostAndSkillSerializer(serializers.ModelSerializer):
    contact_person = EmployerSerializer(read_only=True)
    skills = JobSkillOutboundSerializer(many=True, read_only=True)

    class Meta:
        model = JobPost
        fields = ('id', 'name', 'description', 'city', 'required_education', 'skills', 'contact_person', 'pay_type', 'pay', 'equiv_annual_salary', 'date_posted', 'state', 'hired_person')
        read_only_fields =  ('id', 'name', 'description', 'city', 'required_education', 'skills', 'contact_person', 'pay_type', 'pay', 'equiv_annual_salary', 'date_posted', 'state', 'hired_person')

class JobMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMatch
        fields = ('id', 'job', 'candidate', 'created_by', 'score', 'state')
        read_only_fields = ('job', 'candidate', 'created_by')

class JobMatchAndCandidateSerializer(serializers.ModelSerializer):
    job = BasicJobPostSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = JobMatch
        fields = ('id', 'job', 'candidate', 'created_by', 'score', 'state')
        read_only_fields = ('id', 'job', 'candidate', 'created_by', 'score', 'state')

class JobMatchAndPostSerializer(serializers.ModelSerializer):
    job = JobPostSerializer(read_only=True)

    class Meta:
        model = JobMatch
        fields = ('id', 'job', 'candidate', 'created_by', 'score', 'state')
        read_only_fields = ('id', 'job', 'candidate', 'created_by', 'score', 'state')

class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Token
        fields = ('key', 'user')
        depth = 1

class FavouritesCandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouritesCandidates
        fields = ('candidate', 'SSUser')

class FavouritesJobsInboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouritesJobs
        fields = ('job', 'SSUser')

class FavouritesJobsOutboundSerializer(serializers.ModelSerializer):
    job = BasicJobPostSerializer(read_only=True)

    class Meta:
        model = FavouritesJobs
        fields = ('job', 'SSUser')
