from datetime import datetime
from decimal import Decimal
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from django.core.exceptions import ValidationError
from .models import Candidate, Employer, Recruiter

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        first_name = request.data.get('first_name').strip()
        if first_name == '':
            raise ValidationError('First name cannot be blank.')
        last_name = request.data.get('last_name').strip()
        if last_name == '':
            raise ValidationError('Last name cannot be blank.')
        role = request.data.get('role')
        if role == 'C':
            try:
                dob = datetime.strptime(request.data.get('date_of_birth'), '%Y-%m-%d')
            except:
                # Make the error message more meaningful to the user.
                raise ValidationError('Date of Birth is not in the correct format.')
            gender=request.data.get('gender')
            if gender == '':
                gender = 'N'
            elif gender not in {'M', 'F', 'N'}:
                raise ValidationError('Invalid gender: ' + gender)
            highest_education = request.data.get('highest_education')
            if highest_education == '':
                highest_education = 0
            else:
                highest_education = int(highest_education)
                if highest_education < 0 or highest_education > 9:
                    raise ValidationError('Invalid value for highest education: ' + highest_education)
            looking_for_work = request.data.get('looking_for_work')
            minimum_salary = request.data.get('minimum_salary')
            if minimum_salary == '':
                minimum_salary = 0
            minimum_salary = Decimal(minimum_salary)
        elif role == 'E' or role == 'R':
            company = request.data.get('company')
            website = request.data.get('website')
        else:
            raise ValidationError('Invalid user type: ' + role)
        user = super().save_user(request, user, form, False)
        user_field(user, 'role', role)
        user_field(user, 'first_name', first_name)
        user_field(user, 'last_name', last_name)
        user_field(user, 'city', request.data.get('city'))
        user_field(user, 'phone', request.data.get('phone'))
        user.save()
        # Create either a Candidate or a Employer depending on role.
        if role == 'C':
            Candidate.objects.update_or_create(user=user, date_of_birth=dob,
                gender=gender, highest_education=highest_education,
                looking_for_work=looking_for_work,
                minimum_salary=minimum_salary)
        elif role == 'E':
            Employer.objects.update_or_create(user=user, company=company,
                website=website)
        else:
            Recruiter.objects.update_or_create(user=user, company=company,
                website=website)
        return user
