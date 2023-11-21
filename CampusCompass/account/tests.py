from django.test import TestCase
from django.contrib.auth.models import User
from branch.models import Department, Branch
from .models import Student, Mentor, Club, ClubMember
from .tokens import account_activation_token
from django.urls import reverse
from taggit.models import Tag
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC



class ModelTestCase(TestCase):
    def setUp(self):
        # Create test objects for dependencies
        self.department = Department.objects.create(department_name='Test Department')
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        # Create a test student
        self.student = Student.objects.create(
            student_id='SRN123',
            bio='Test Bio',
            user=self.user,
            department=self.department,
            branch=self.branch,
            college_email='test@example.com',
            whatsapp_number='1234567890',
            whatsapp_link='http://example.com',
            email_confirmed=True,
            is_mentor=False,
            show_number=True,
            year_of_passing_out=2023
        )

    def test_mentor_model(self):

        mentor = Mentor.objects.create(
            student=self.student,
            resume='path/to/resume.pdf',
            description='Test Mentor Description',
            approved=True
        )
        domain_name = "aiml"
        domain, created = Tag.objects.get_or_create(name=domain_name)
        mentor.domain.add(domain)
        self.assertTrue(mentor.approved)

        # Add mentorship-related assertions here
        # For example, you can check if the mentor is associated with the correct student
        self.assertEqual(mentor.student, self.student)

    def test_club_member_model(self):
        club = Club.objects.create(
            club_name='Test Club',
            club_desc='Test Club Description',
            club_logo="/path/to/logo.jpg"
        )

        club_member = ClubMember.objects.create(
            user=self.user,
            club=club,
            club_head=True,
            social_media_manager=False
        )

        # Adjust the expected result based on your __str__ implementation
        self.assertEqual(club_member.__str__(), 'testuser (Test Club)')

    def test_club_model(self):
        club = Club.objects.create(
            club_name='Test Club',
            club_desc='Test Club Description',
            club_logo="/path/to/logo.jpg"
        )

        club.branch.add(self.branch)

        self.assertEqual(club.__str__(), 'Test Club')


class AccountViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        # Create a student for the user
        self.student = Student.objects.create(
            student_id='SRN123',
            bio='Test Bio',
            user=self.user,
            college_email='test@pesu.pes.edu',
            whatsapp_number='1234567890',
            year_of_passing_out=2023
        )

        # Create a club for testing
        self.club = Club.objects.create(
            club_name='Test Club',
            club_desc='Test Club Description'
        )

    def test_register_view(self):
        # Test the register view
        response = self.client.get('/account/register')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        # Test the login view
        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        # Test the profile view
        response = self.client.get('/account/profile')
        self.assertEqual(response.status_code, 302)  # Redirects to login because user is not authenticated

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get('/account/profile')
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        # Test the edit profile view
        response = self.client.get('/account/edit_profile')
        self.assertEqual(response.status_code, 302)  # Redirects to login because user is not authenticated

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get('/account/edit_profile')
        self.assertEqual(response.status_code, 200)

    def test_mentor_registration_view(self):
        # Test the mentor registration view
        response = self.client.get('/account/mentor_registration')
        self.assertEqual(response.status_code, 302)  # Redirects to login because user is not authenticated

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get('/account/mentor_registration')
        self.assertEqual(response.status_code, 200)

        # Test submitting mentor registration form
        response = self.client.post('/account/mentor_registration', {'fileupload': 'test_resume.pdf', 'domains': 'Domain1, Domain2', 'description': 'Test description'})
        self.assertEqual(response.status_code, 302)  # Redirects to profile after submission

    
    def test_approve_membership_view(self):
        # Test the approve membership view
        response = self.client.get('/account/approve_membership')
        self.assertEqual(response.status_code, 302)  # Redirects to login because user is not authenticated

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get('/account/approve_membership')
        self.assertEqual(response.status_code, 302)

        # Test submitting approve membership form
        response = self.client.post('/account/approve_membership', {'srn': 'SRN123', 'social_media_manager': True})
        self.assertEqual(response.status_code, 302)  # Redirects to profile after submission


class AccountActivationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='activation_test_user',
            password='testpassword',
            email='activation_test@example.com'
        )
        
        # Try to get an existing Student object
        student = Student.objects.filter(user=self.user).first()

        # If no existing Student, create a new one
        if not student:
            student = Student.objects.create(user=self.user)
        
        # If the student is newly created, set email_confirmed to True for testing
        if not student.email_confirmed:
            student.email_confirmed = True
            student.save()

        self.user.student = student

    def test_account_activation(self):
        # Test the account activation process
        token = account_activation_token.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

        # Ensure the user has a related student object before accessing student attributes
        if not hasattr(self.user, 'student') or not self.user.student:
            self.user.student = Student.objects.create(user=self.user)
        self.user.student.email_confirmed = True  # Set email_confirmed to True for testing
        self.user.save()

        response = self.client.get(reverse('activate', args=[uidb64, token]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful activation

