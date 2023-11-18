from django.test import TestCase
from django.contrib.auth.models import User
from branch.models import Department, Branch
from .models import Student, Mentor, Club, ClubMember
from taggit.models import Tag

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
            username='mentor_user',
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
