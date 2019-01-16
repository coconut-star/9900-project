from django.test import TestCase
from .models import Candidate
from django.contrib.auth.models import User

# Create your tests here.
class ModelTestCase(TestCase):
    def setUp(self):
        self.candidate = Candidate()
        self.candidate.name = 'person1'
        self.candidate.city = 'Sydney'
        self.candidate.email = 'person1@xxx.com'
        self.candidate.date_of_birth = '1990-01-01'
        self.user = User()

    def test_model_can_create_a_person(self):
        old_count = Candidate.objects.count()
        self.user.save()
        self.candidate.user_id = self.user.id
        self.candidate.save()
        new_count = Candidate.objects.count()
        self.assertNotEqual(old_count, new_count)
