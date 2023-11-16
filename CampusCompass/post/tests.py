from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, PostComment, Branch,Department

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