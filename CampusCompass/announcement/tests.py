from django.test import TestCase
from django.contrib.auth.models import User
from .models import Announcement, Branch
from branch.models import Department


class AnnouncementModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a department for testing
        self.department = Department.objects.create(department_name='Test Department')

        # Create a branch for testing
        self.branch = Branch.objects.create(
            branch_name='Test Branch',
            department=self.department
        )

        # Create an announcement for testing
        self.announcement = Announcement.objects.create(
            title='Test Announcement',
            content='This is a test announcement.',
            featured_img='path/to/testimage.jpg',
            post_by=self.user
        )
        self.announcement.branch.add(self.branch)

    def test_announcement_str_method(self):
        print("Running test_announcement_str_method")
        self.assertEqual(str(self.announcement), 'Test Announcement')

    def test_get_model_name_method(self):
        print("Running test_get_model_name_method")
        self.assertEqual(self.announcement.get_model_name(), 'Announcement')

    def test_announcement_search_method(self):
        print("Running test_announcement_search_method")
        qs = Announcement.objects.search(query='Test')
        self.assertIn(self.announcement, qs)

    def test_announcement_image_upload(self):
        print("Running test_announcement_image_upload")
        # Test that the featured image is uploaded successfully
        self.assertIsNotNone(self.announcement.featured_img.path)

    def test_announcement_branch_relationship(self):
        print("Running test_announcement_branch_relationship")
        # Test that the announcement is associated with the correct branch
        self.assertEqual(self.announcement.branch.count(), 1)
        self.assertEqual(self.announcement.branch.first(), self.branch)

    def test_announcement_date_created(self):
        print("Running test_announcement_date_created")
        # Test that the date_created field is set automatically
        self.assertIsNotNone(self.announcement.date_created)

# Add more tests as needed based on your model's functionality
