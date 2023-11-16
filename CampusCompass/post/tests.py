from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, PostComment, Branch,Department
from .forms import PostForm

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch',department=self.department)
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author='Test Author',
        )
        self.post.branch.add(self.branch)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, 'Test Author')
        self.assertEqual(self.post.get_model_name(), 'Post')

class PostCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch',department=self.department)
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post',
            slug='test-post',
            content='This is a test post.',
            author='Test Author',
            
        )
        self.post.branch.add(self.branch)
        
        self.comment = PostComment.objects.create(
            user=self.user,
            comment='This is a test comment.',
            post=self.post,
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.comment, 'This is a test comment.')
        self.assertEqual(str(self.comment.user), 'testuser')


class PostFormTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch',department=self.department)
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_form(self):
        form_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'tags': 'test, post',
            'branch': [self.branch],
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Test Post')
        self.assertEqual(form.cleaned_data['content'], 'This is a test post.')
        self.assertEqual(list(form.cleaned_data['branch']), [self.branch])


class MakePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch',department=self.department)
        self.url = reverse('make_post')  # replace 'make_post' with the actual name of the view

    def test_make_post_view_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_make_post_view_POST(self):
        self.client.login(username='testuser', password='12345')
        form_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
            'tags': 'test, post',
            'branch': [self.branch],
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)