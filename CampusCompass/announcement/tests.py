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

    def test_announcement_creation_view(self):
        # Test F001: Announcement Creation
        self.client.force_login(self.club_head_user)

        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

        # Assuming your HTML form contains these fields
        form_data = {
            'title': 'Test Announcement',
            'content': 'This is a test announcement.',
            'featured_img': '',  # Replace with the actual file data if needed
        }

        form = AnnouncementForm(data=form_data)

        if not form.is_valid():
            print(form.errors)
        self.assertFalse(form.is_valid())
        
        response = self.client.post(reverse('create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Announcement.objects.filter(title='Test Announcement').exists())

    def test_announcement_date_created(self):
        print("Running test_announcement_date_created")
        # Test that the date_created field is set automatically
        self.assertIsNotNone(self.announcement.date_created)

# Add more tests as needed based on your model's functionality
