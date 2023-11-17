from django.test import TestCase
from django.contrib.auth.models import User
from .models import Announcement, Branch
from django.db import models
from django.contrib.auth.models import User
from branch.models import *
from branch.models import Department,Branch
from taggit.managers import TaggableManager

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
