from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Resource
from .forms import ResourceForm
from .views import upload_resource

class ResourceTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.resource = Resource.objects.create(
            user=self.user,
            title='Test Resource',
            files='C:/Se_project/Campus_Compass/Campus-Compass/CampusCompass/resource',  # Provide a valid file path for testing
        )

    # ... (unchanged code above)

    def test_upload_resource_view(self):
        # Simulate a user session
        self.client.force_login(self.user)

        # Define the URL using reverse
        url = reverse('upload_resource')

        # Define the data for the post request
        data = {
            'title': 'Test Resource',
            'files': 'path/to/test/file.txt',  # Provide a valid file path for testing
            'branch': [1],  # Assuming 1 is a valid branch ID for testing
            'tags': 'tag1,tag2',  # Provide tags separated by commas for testing
        }

        # Call the view function
        response = self.client.post(url, data=data)

        # Check if the resource is created and the user is redirected
        self.assertEqual(response.status_code, 302)
    def test_resource_view_status_code(self):
        # Test the status code of the resource view
        response = self.client.get(reverse('resource'))
        self.assertEqual(response.status_code, 200)  # Assuming 'resource' is a valid URL

    def test_resource_by_tag_view(self):
        # Test the resource by tag view
        response = self.client.get(reverse('search', args=['tag1']))
        self.assertEqual(response.status_code, 200)  # Assuming 'search' is a valid URL

    def test_edit_resource_view(self):
        # Simulate a user session
        self.client.force_login(self.user)

        # Call the edit_resource view
        response = self.client.post(reverse('edit_resource', args=[self.resource.id]), data={
            'title': 'Updated Test Resource',
            'branch': [1],
            'tags': 'tag3,tag4',
        })

        # Check if the resource is updated in the database
        updated_resource = Resource.objects.get(id=self.resource.id)
        self.assertEqual(updated_resource.title, 'Updated Test Resource')
        self.assertEqual(updated_resource.tags.count(), 2)

    # ... (unchanged code above)

    def test_download_resource_view(self):
        # Simulate a user session
        self.client.force_login(self.user)

        # Call the download_resource view
        response = self.client.get(reverse('download_resource', args=[self.resource.id]))
        self.assertEqual(response.status_code, 200)  # Assuming 'download_resource' returns the file content

