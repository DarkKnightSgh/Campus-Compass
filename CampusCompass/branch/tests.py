from django.test import TestCase, Client
from .models import Branch, Department
from django.urls import reverse
import json

class DepartmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(department_name='Test Department')

    def test_department_name_content(self):
        expected_object_name = f'{self.department.department_name}'
        self.assertEquals(expected_object_name, str(self.department))
    
    def test_department_id_auto_created(self):
        self.assertIsNotNone(self.department.department_id)

    def test_department_name_not_empty(self):
        self.assertNotEquals(self.department.department_name, '')

    def test_department_name_is_string(self):
        self.assertIsInstance(self.department.department_name, str)

class BranchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(department_name='Test Department')
        cls.branch = Branch.objects.create(branch_name='Test Branch', department=cls.department)

    def test_branch_name_content(self):
        expected_object_name = f'{self.branch.branch_name} ({self.branch.department})'
        self.assertEquals(expected_object_name, str(self.branch))

    def test_branch_code_auto_created(self):
        self.assertIsNotNone(self.branch.branch_code)

    def test_branch_has_department(self):
        self.assertEquals(self.branch.department, self.department)

    def test_branch_name_not_empty(self):
        self.assertNotEquals(self.branch.branch_name, '')
    
    def test_branch_department_is_instance_of_department(self):
        self.assertIsInstance(self.branch.department, Department)

    def test_branch_name_is_string(self):
        self.assertIsInstance(self.branch.branch_name, str)

    def test_branch_code_is_integer(self):
        self.assertIsInstance(self.branch.branch_code, int)
    
    
    

class GetBranchesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(department_name='Test Department')
        number_of_branches = 5
        for branch_num in range(number_of_branches):
            Branch.objects.create(branch_name=f'Branch {branch_num}', department=cls.department)

    def setUp(self):
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))  
        self.assertEqual(response.status_code, 200)

    def test_view_returns_correct_data(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))  
        self.assertEqual(response.status_code, 200)
        branches = json.loads(response.content)['branches']
        self.assertEqual(len(branches), 5)
        for branch in branches:
            self.assertIn('branch_code', branch)
            self.assertIn('branch_name', branch)
    
    def test_view_returns_json(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))
        self.assertEqual(response['content-type'], 'application/json')

    def test_view_returns_correct_number_of_branches(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))
        branches = json.loads(response.content)['branches']
        self.assertEqual(len(branches), 5)

    def test_view_returns_branches_with_correct_department_name(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))
        branches = json.loads(response.content)['branches']
        for branch in branches:
            # get department from branch_code
            branch_code = branch['branch_code']
            branch = Branch.objects.get(branch_code=branch_code )
            expected_department = branch.department
            self.assertEqual(expected_department.department_name, self.department.department_name)

    def test_view_returns_branches_with_correct_department_id(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))
        branches = json.loads(response.content)['branches']
        for branch in branches:
            # get department from branch_code
            branch_code = branch['branch_code']
            branch = Branch.objects.get(branch_code=branch_code )
            expected_department = branch.department
            self.assertEqual(expected_department.department_id, self.department.department_id)

    def test_view_returns_no_branches_for_nonexistent_department(self):
        response = self.client.get(reverse('get_branches', args=[999]))  # assuming 999 is an ID that doesn't exist
        branches = json.loads(response.content)['branches']
        self.assertEqual(len(branches), 0)

    def test_view_returns_no_branches_for_empty_department(self):
        response = self.client.get(reverse('get_branches', args=[self.department.department_id]))
        branches = json.loads(response.content)['branches']
        self.assertEqual(len(branches), 5)
        id= self.department.department_id
        self.department.delete()
        response = self.client.get(reverse('get_branches', args=[id]))
        branches = json.loads(response.content)['branches']
        self.assertEqual(len(branches), 0)

