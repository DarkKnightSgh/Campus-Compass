# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Post
from resource.models import Resource
from announcement.models import Announcement
from account.models import Student

class SearchViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create some test data (adjust as needed)
        self.post = Post.objects.create(title='Test Post', content='Test content')
        self.resource = Resource.objects.create(title='Test Resource', description='Test description')
        self.announcement = Announcement.objects.create(title='Test Announcement', content='Test content')
        self.student = Student.objects.create(user=self.user, bio='Test bio')

        # Create a test client
        self.client = Client()

    def test_search_view(self):
        # Assume you have a URL named 'search' in your urls.py
        url = reverse('search')

        # Test with a valid query
        response = self.client.post(url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

        # Add more assertions based on your specific use case and expected behavior

    def test_search_view_no_query(self):
        # Test with no query
        url = reverse('search')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertEqual(response.context['count'], 0)

    def test_search_view_invalid_query(self):
        # Test with an invalid query
        url = reverse('search')
        response = self.client.post(url, {'q': '!@#$%^'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
        self.assertEqual(response.context['count'], 0)

    # Add more test cases as needed

