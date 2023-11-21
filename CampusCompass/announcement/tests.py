from django.test import TestCase
from django.contrib.auth.models import User
from .models import Announcement, Branch
from django.db import models
from django.contrib.auth.models import User
from branch.models import *
from branch.models import Department,Branch
from taggit.managers import TaggableManager
from django.urls import reverse
from .forms import AnnouncementForm
from .views import create

from django.db.models import Q


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
            post_by=self.user
        )
        self.announcement.branch.add(self.branch)

    def test_announcement_str_method(self):
        self.assertEqual(str(self.announcement), 'Test Announcement')

    def test_get_model_name_method(self):
        self.assertEqual(self.announcement.get_model_name(), 'Announcement')

    def test_announcement_search_method(self):
         qs = Announcement.objects.search(query='Test')
         self.assertIn(self.announcement, qs)


class AnnouncementTestCase(TestCase):

    def setUp(self):
        # Create a user with club head role
        self.club_head_user = User.objects.create_user(username='clubhead', password='password')
        self.club_head_user.groups.create(name='club_head_group')

        # Create a user with social media manager role
        self.social_media_manager_user = User.objects.create_user(username='socialmedia', password='password')
        self.social_media_manager_user.groups.create(name='social_media_manager_group')

    def test_announcement_creation_view(self):
        # Test F001: Announcement Creation
        self.client.force_login(self.club_head_user)

        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

        # Assuming your HTML form contains these fields
        form_data = {
            'title': 'Test Announcement',
            'content': 'This is a test announcement.',
            'featured_img': None,  # Replace with the actual file data if needed
        }

        form = AnnouncementForm(data=form_data)

        if not form.is_valid():
            print(form.errors)
        self.assertFalse(form.is_valid())
        
        response = self.client.post(reverse('create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Announcement.objects.filter(title='Test Announcement').exists())

    def test_access_control_decorator(self):
        # Test F002: Access Control Decorator
        self.client.force_login(self.club_head_user)
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)  # Should return 302 for club head

        self.client.force_login(self.social_media_manager_user)
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)  # Should return 302 for social media manager

        # Create a regular user (not in any special group)
        regular_user = User.objects.create_user(username='regularuser', password='password')
        self.client.force_login(regular_user)
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)  # Should return 403 for regular user
