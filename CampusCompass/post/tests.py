from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from .models import Post, PostComment, Branch,Department
from account.models import Student
from taggit.models import Tag

from .forms import PostForm

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
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
        

class DeletePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', content='Test Content', user=self.user, slug='test-post')

    def test_delete_post(self):
        # Log in
        self.client.login(username='testuser', password='12345')

        # Delete the post
        response = self.client.post(reverse('delete_post', kwargs={'slug': 'test-post'}))

        # Check that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the post was deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(slug='test-post')
        
        # check if post exists
        self.assertFalse(Post.objects.filter(slug='test-post').exists())

    def tearDown(self):
        # Log out
        self.client.logout()
        


class EditPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch',department=self.department)
        self.new_branch = Branch.objects.create(branch_name='New Test Branch',department=self.department)
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

    def test_edit_post(self):
        # Log in
        self.client.login(username='testuser', password='12345')

        # Edit the post
        response = self.client.post(reverse('edit_post', kwargs={'slug': self.post.slug}), {
            'title': 'Updated Post',
            'content': 'Updated Content',
            'branch': [self.new_branch.branch_code],
            'tags': 'updatedtag',
        })

        # Check that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the post was updated
        post = Post.objects.get(post_id=self.post.post_id)
        self.assertEqual(post.title, 'Updated Post')
        self.assertEqual(post.content, 'Updated Content')
        self.assertIn(self.branch, post.branch.all())
        self.assertIn('updatedtag', [tag.name for tag in post.tags.all()])

    def tearDown(self):
        # Log out
        self.client.logout()
        

class MakePostViewSeleniumTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
        Branch.objects.all().delete()
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
        self.browser.set_page_load_timeout(120)

    def tearDown(self):
        self.browser.close()
        

    def test_make_post_view_POST_creates_post(self):
        self.browser.get(self.live_server_url + '/account/login')  # replace with the actual login url
        username_input = self.browser.find_element(By.NAME,"username")
        password_input = self.browser.find_element(By.NAME,"password")
        username_input.send_keys('testuser')
        password_input.send_keys('12345')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.browser, 2).until(
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
        # branch_checkbox_id = f"id_branch_{branch_code}"
        branch_checkbox_id = f"id_branch_0"
        branch_checkbox = self.browser.find_element(By.ID, branch_checkbox_id)
        
        
        branch_checkbox = self.browser.find_element(By.ID, branch_checkbox_id)
        branch_checkbox.send_keys(Keys.SPACE)
        

        is_selected = branch_checkbox.is_selected()
        self.assertTrue(is_selected, "The checkbox was not selected.")
        
        branch_checkbox.send_keys(Keys.RETURN)
        
        
        self.assertTrue(Post.objects.filter(title='Test Post').exists())
        

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)
        self.student = Student.objects.create(student_id="PES12736437",
                                              user=self.user,
                                              department=self.department,
                                              branch=self.branch,
                                              whatsapp_number="+91992636672",
                                              year_of_passing_out=2024,
                                            )
        self.post = Post.objects.create(
            title='Test Post', 
            content ="test data",
            user = self.user,
            slug="test-post",
        )
        self.tag = Tag.objects.create(name='Test Tag')
        
        self.post.tags.add(self.tag)
        self.post.branch.add(self.branch)

    def test_feed_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_add_comment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('comment_on_post', args=[self.post.slug]), {'comment': 'Test Comment'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(PostComment.objects.filter(comment='Test Comment').exists())

    def test_tag_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('tag_post', args=[self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.department = Department.objects.create(department_name="test_dept")
        self.branch = Branch.objects.create(branch_name='Test Branch', department=self.department)
        self.student = Student.objects.create(student_id="PES12736437",
                                              user=self.user,
                                              department=self.department,
                                              branch=self.branch,
                                              whatsapp_number="+91992636672",
                                              year_of_passing_out=2024,
                                            )
        self.post = Post.objects.create(
            title='Test Post', 
            content ="test data",
            user = self.user,
            slug="test-post",
        )
        self.tag = Tag.objects.create(name='Test Tag')
        
        self.post.tags.add(self.tag)
        self.post.branch.add(self.branch)
        self.comment = PostComment.objects.create(user=self.user, post=self.post, comment='Test Comment')

    def test_post_detail_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test Comment')
    def test_add_comment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('comment_on_post', args=[self.post.slug]), {'comment': 'Test Comment'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(PostComment.objects.filter(comment='Test Comment').exists())




class FeedViewSeleniumTest(StaticLiveServerTestCase):
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
        self.post = Post.objects.create(
            title='Test Post', 
            content ="test data",
            user = self.user,
            slug="test-post",
        )
        self.tag = Tag.objects.create(name='Test Tag')
        
        self.post.tags.add(self.tag)
        self.post.branch.add(self.branch)
        self.browser.set_page_load_timeout(120)
        
    
    def tearDown(self):
        self.browser.close()
        
    def test_feed_view(self):
        self.browser.get(self.live_server_url + '/account/login')  # replace with the actual login url
        username_input = self.browser.find_element(By.NAME,"username")
        password_input = self.browser.find_element(By.NAME,"password")
        username_input.send_keys('testuser')
        password_input.send_keys('12345')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + '/account/profile')  
        )
        # Navigate to the feed page
        self.browser.get(self.live_server_url + '/post/feed') 
        # wait
        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + '/post/feed')  
        )
        # Check that the feed page is displayed
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('My Feed', body.text)
        self.assertIn(self.post.title, body.text)

    def test_add_comment(self):
        # Log in
        self.browser.get(self.live_server_url + '/account/login')
        username_input = self.browser.find_element(By.NAME,"username")
        password_input = self.browser.find_element(By.NAME,"password")
        username_input.send_keys('testuser')
        password_input.send_keys('12345')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + '/account/profile')
        )

        # Navigate to the post detail page
        self.browser.get(self.live_server_url + '/post/' + self.post.slug)

        # Fill in the comment form
        comment_input = self.browser.find_element(By.NAME, 'comment')
        comment_input.send_keys('Test Comment')

        # Submit the form
        comment_input.submit()

        # Wait for the page to reload
        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + '/post/' + self.post.slug)
        )

        # Check that the comment was added
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Test Comment', body.text)
        
class FeedTagViewSeleniumTest(StaticLiveServerTestCase):
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
        self.post = Post.objects.create(
            title='Test Post', 
            content ="test data",
            user = self.user,
            slug="test-post",
        )
        self.tag = Tag.objects.create(name='Test Tag')
        
        self.post.tags.add(self.tag)
        self.post.branch.add(self.branch)
        self.browser.set_page_load_timeout(120)
    
    def tearDown(self):
        self.browser.close()
        
    def test_feed_view(self):
        self.browser.get(self.live_server_url + '/account/login')  # replace with the actual login url
        username_input = self.browser.find_element(By.NAME,"username")
        password_input = self.browser.find_element(By.NAME,"password")
        username_input.send_keys('testuser')
        password_input.send_keys('12345')
        password_input.send_keys(Keys.RETURN)
        
        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + '/account/profile')  
        )
        slug=self.tag.slug
        # Navigate to the feed page
        self.browser.get(self.live_server_url + f'/post/tag/{slug}') 
        # wait
        WebDriverWait(self.browser, 2).until(
            EC.url_to_be(self.live_server_url + f'/post/tag/{slug}')  
        )
        # Check that the feed page is displayed
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(self.post.title, body.text)
        self.assertIn(self.tag.name, body.text)
        
