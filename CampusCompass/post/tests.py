from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from .models import Post, PostComment, Branch,Department
from account.models import Student

from .forms import PostForm

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


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
        

class MakePostViewSeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # replace with the Chrome webdriver
        self.user = User.objects.create_user(username='testuser', password='12345',email="test@example.com")
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)
        self.student = Student.objects.create(student_id="PES12736437",
                                              user=self.user,
                                              department=self.department,
                                              branch=self.branch,
                                              whatsapp_number="+91992636672",
                                              year_of_passing_out=2024,
                                            )
        # Log in the test user
        self.client.login(username='testuser', password='12345')
        print(self.live_server_url)


    def tearDown(self):
        self.browser.close()
        

    def test_make_post_view_POST_creates_post(self):
        self.browser.get(self.live_server_url + '/account/login')  # replace with the actual login url
        username_input = self.browser.find_element(By.NAME,"username")
        password_input = self.browser.find_element(By.NAME,"password")
        username_input.send_keys('testuser')
        password_input.send_keys('12345')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.browser, 1).until(
            EC.url_to_be(self.live_server_url + '/account/profile')  
        )

        self.browser.get(self.live_server_url + '/post/make_post')  # replace with the actual make post url
        title_input = self.browser.find_element(By.ID,"id_title")
        content_input = self.browser.find_element(By.ID,"id_content")
        tags_input = self.browser.find_element(By.ID,"id_tags")
        branch_input = self.browser.find_element(By.ID,"id_branch")
        title_input.send_keys('Test Post')
        content_input.send_keys('This is a test post.')
        tags_input.send_keys('test, post')
        
        branch_code = str(int(self.branch.branch_code)-1)
        branch_checkbox_id = f"id_branch_{branch_code}"
        branch_checkbox = self.browser.find_element(By.ID, branch_checkbox_id)
        
        
        branch_checkbox = self.browser.find_element(By.ID, branch_checkbox_id)
        branch_checkbox.send_keys(Keys.SPACE)
        

        is_selected = branch_checkbox.is_selected()
        self.assertTrue(is_selected, "The checkbox was not selected.")
        
        branch_checkbox.send_keys(Keys.RETURN)
        
        
        self.assertTrue(Post.objects.filter(title='Test Post').exists())