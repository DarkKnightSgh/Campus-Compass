# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Post
from resource.models import Resource
from announcement.models import Announcement
from account.models import Student
from branch.models import Branch,Department
from taggit.models import Tag

class SearchViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)
        self.student = Student.objects.create(student_id="PES12736437",
                                              user=self.user,
                                              department=self.department,
                                              branch=self.branch,
                                              whatsapp_number="+91992636672",
                                              year_of_passing_out=2024,
                                            )

        # Create some test data (adjust as needed)
        self.post = Post.objects.create(
            title='Test Post', 
            content ="test data",
            user = self.user,
            slug="test-post",
        )
        self.tag = Tag.objects.create(name='Test Tag')
        
        self.post.tags.add(self.tag)
        self.post.branch.add(self.branch)
        
        self.resource = Resource.objects.create(user=self.user,title='Test Resource', files='Test description')
        self.resource.branch.add(self.branch)
        self.resource.tags.add(self.tag)
        
        self.announcement = Announcement.objects.create(post_by=self.user,title='Test Announcement', content='Test content')
        self.announcement.branch.add(self.branch)

        # Create a test client
        self.client = Client()

    def test_search_view(self):
        # Assume you have a URL named 'search' in your urls.py
        url = reverse('search')

        # Test with a valid query
        response = self.client.post(url, {'q': 'Test'})
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

