from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User

USER_ROLES = (('A', 'Administrator'), ('C', 'Candidate'), ('E', 'Employer'), ('R', 'Recruiter'))

GENDERS = (('M', 'Male'), ('F', 'Female'), ('N', 'Not Specified'))

SKILL_TYPES = (('C', 'Category'), ('L', 'Leaf'))

DOCUMENT_TYPES = (('T', 'Academic Transcript'), ('E', 'Cerfificate'), ('C', 'Curriculum Vitae'),  ('R', 'Reference'), ('O', 'Other'))

EDUCATION_LEVELS = ((0, 'None'), (1, 'High School'), (2, 'Certificate'), (3, 'Associate Diploma'), (4, 'Diploma'),
    (5, 'Bachelor\'s Degree'), (6, 'Graduate Certificate'), (7, 'Graduate Diploma'), (8, 'Master\'s Degree'),
    (9, 'Ph.D'))

PAY_TYPES = (('H', 'Hourly'), ('D', 'Daily'), ('M', 'Monthly'), ('Y', 'Yearly'))

JOB_STATES = (('L', 'Looking for Candidates'), ('F', 'Position Filled'), ('JO', 'Job Offer Made'), ('W', 'Position Withdrawn'))

MATCH_STATES = (
    ('N', 'No Action Taken'),
    ('CI', 'Candidate Interested'),
    ('EI', 'Employer Interested'),
    ('P', 'In Progress'),
    ('DC', 'Declined by Candidate'),
    ('DE', 'Declined by Employer'),
    ('JO', 'Job Offer Made'),
    ('H', 'Hired'),
    ('JD', 'Job Offer Declined'),
    ('F', 'Position Filled'),
    ('W', 'Position Withdrawn')
)

class Skill(models.Model):
    category = models.ForeignKey('self', null=True, related_name='skill', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=128, blank=False)
    type = models.CharField(max_length=1, choices=SKILL_TYPES, blank=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = ('category', 'name',)

class SSUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        return SSUser(email=email, first_name=first_name, last_name=last_name, password=password)

    def create_superuser(self, email, first_name, last_name, password):
        return SSUser(email=email, first_name=first_name, last_name=last_name, password=password)

class SSUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, blank=False, unique=True)
    phone = models.CharField(max_length=16, blank=True)
    role = models.CharField(max_length=1, choices=USER_ROLES)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    city = models.CharField(max_length=128, blank=False, unique=False)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = SSUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class Role(models.Model):
    user = models.OneToOneField(SSUser, primary_key=True, on_delete=models.CASCADE)
    def __str__(self):
        return "{}, {}".format(self.user.last_name, self.user.first_name)

    class Meta:
        abstract = True

class Admin(Role):
    pass

class Candidate(Role):
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    highest_education = models.PositiveIntegerField(choices=EDUCATION_LEVELS, default=0)
    looking_for_work = models.BooleanField(default=True)
    minimum_salary = models.DecimalField(decimal_places=0, max_digits=10, default=0)
    photo = models.CharField(max_length=64, blank=True)

class Employer(Role):
    company = models.CharField(max_length=128, blank=True, unique=False)
    website = models.CharField(max_length=128, blank=True, unique=False)
    photo = models.CharField(max_length=64, blank=True)

class Recruiter(Role):
    company = models.CharField(max_length=128, blank=True, unique=False)
    website = models.CharField(max_length=128, blank=True, unique=False)
    photo = models.CharField(max_length=64, blank=True)

class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    filename = models.CharField(max_length=64, blank=False)
    type = models.CharField(max_length=1, choices=DOCUMENT_TYPES, blank=False)
    description = models.CharField(max_length=64, blank=False)
    date_uploaded = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.candidate, self.filename)

    class Meta:
        unique_together = ('candidate', 'filename',)

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.PositiveIntegerField()
    months_experience = models.PositiveIntegerField(default=0)
    evidence = models.ManyToManyField(Document, blank=True)

    @property
    def experience_unit(self):
        if self.months_experience % 12 == 0:
            return 12
        else:
            return 1

    @property
    def experience(self):
        return self.months_experience // self.experience_unit

    def __str__(self):
        return "{} {}".format(self.candidate, self.skill)

    class Meta:
        unique_together = ('candidate', 'skill',)

class JobPost(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    city = models.CharField(max_length=128, blank=False, unique=False)
    required_education = models.PositiveIntegerField(choices=EDUCATION_LEVELS, default=0)
    contact_person = models.ForeignKey(Employer, null=False, on_delete=models.CASCADE)
    pay_type = models.CharField(max_length=1, choices=PAY_TYPES)
    pay = models.DecimalField(decimal_places=2, max_digits=10)
    # This field is redundant, but storing it greatly speeds up the task of
    # filtering JobPosts by salary, at the cost of a little extra database
    # space.
    equiv_annual_salary = models.DecimalField(decimal_places=0, max_digits=10, default=0)
    date_posted = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=2, choices=JOB_STATES, default='L')
    hired_person = models.ForeignKey(Candidate, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    # Convert monthly or hourly pay to the equivalent annual salary. This doesn't have
    # to be exact - it's only used to avoid offering jobs to candidates if the pay is
    # too low for them.

    def EquivalentAnnualSalary(pay_type, pay):
        if pay_type == 'Y':
            return pay
        if pay_type == 'M':
            return pay * 12
        # Convert hourly pay based on a 40 hour week with 4 weeks annual leave.
        return pay * 48 * 40

class JobSkill(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()
    proficiency = models.PositiveIntegerField()
    months_experience = models.PositiveIntegerField(default=0)

    @property
    def experience_unit(self):
        if self.months_experience % 12 == 0:
            return 12
        else:
            return 1

    @property
    def experience(self):
        return self.months_experience // self.experience_unit

    def __str__(self):
        return "{} {}".format(self.job.name, self.skill.name)

    class Meta:
        unique_together = ('job', 'skill',)

class JobMatch(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, null=False, on_delete=models.CASCADE)
    # created_by will be null for automatically created matches.
    created_by = models.ForeignKey(SSUser, null=True, on_delete=models.SET_NULL)
    score = models.PositiveIntegerField(blank=False, unique=False)
    state = models.CharField(max_length=2, choices=MATCH_STATES, default='N')

    def __str__(self):
        return "{} {}".format(self.job.name, self.candidate)

    def IsActive(self):
        return self.state not in { 'DC', 'DE','H', 'JD', 'F', 'W' }

    class Meta:
        unique_together = ('job', 'candidate',)

class FavouritesCandidates(models.Model):
    candidate = models.ForeignKey(Candidate, null=False, on_delete = models.CASCADE)
    SSUser = models.ForeignKey(SSUser, null = False, on_delete = models.CASCADE)

class FavouritesJobs(models.Model):
    job = models.ForeignKey(JobPost, null=False, on_delete = models.CASCADE)
    SSUser = models.ForeignKey(SSUser, null = False, on_delete = models.CASCADE)