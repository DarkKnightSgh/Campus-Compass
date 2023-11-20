from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Resource, Branch
from taggit.models import Tag
from branch.models import Department

class ResourceModelTestCase(TestCase):
    def setUp(self):
        # Create a test department
        self.department = Department.objects.create(department_name='Test Department')

        # Create test objects for dependencies
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test resource
        # Use SimpleUploadedFile to simulate file upload in tests
        file_content = b'Test file content'
        uploaded_file = SimpleUploadedFile("testfile.txt", file_content, content_type="text/plain")
        self.resource = Resource.objects.create(
            user=self.user,
            title='Test Resource',
            files=uploaded_file,
        )
        self.resource.branch.add(self.branch)

        # Add tags to the resource
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.resource.tags.add(self.tag1, self.tag2)

    def test_resource_storage(self):
        # Test if the uploaded file is stored correctly
        storage = self.resource.files.storage
        file_path = storage.path(self.resource.files.name)

        # Add assertions based on your expected results
        self.assertTrue(storage.exists(file_path))
        self.assertEqual(storage.size(file_path), len(b'Test file content'))
        print("File storage test success!")

    def test_tagging_system(self):
        # Test if tags are associated with the resource correctly
        self.assertTrue(self.tag1 in self.resource.tags.all())
        self.assertTrue(self.tag2 in self.resource.tags.all())
        print("Tagging system test success!")

    def test_branch_selection_interface(self):
        # Test if the branch is associated with the resource correctly
        self.assertEqual(self.resource.branch.count(), 1)
        self.assertEqual(self.resource.branch.first(), self.branch)
        print("Branch selection interface test success!")

    def test_metadata(self):
        # Test metadata such as upload date and user information
        self.assertIsNotNone(self.resource.uploaded_at)
        self.assertEqual(self.resource.user, self.user)
        print("Metadata test success!")

    # Add other tests as needed
