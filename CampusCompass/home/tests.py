from django.test import TestCase
from django.urls import reverse
from .models import ContactUs
from django.core import mail
from django.core.mail import EmailMessage
from django.utils import timezone
import CampusCompass.settings as settings

class ContactUsViewTest(TestCase):
    def test_contact_us_view(self):
        # Define the valid form data
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'query': 'Test query content.',
        }

        # Send a POST request to the contactus view with the valid form data
        response = self.client.post(reverse('contactus'), form_data)

        # Check if the form submission was successful and redirected to the expected URL
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
        self.assertRedirects(response, reverse('contactsuccess'))

        # Check if a ContactUs instance was created with the provided data
        self.assertEqual(ContactUs.objects.count(), 1)
        contact = ContactUs.objects.first()
        self.assertEqual(contact.name, form_data['name'])
        self.assertEqual(contact.email, form_data['email'])
        self.assertEqual(contact.query, form_data['query'])

    def test_contact_us_view_invalid_form(self):
        # Define the invalid form data
        form_data = {
            'name': 'John Doe',
            'email': '',
            'query': 'Test query content.',
        }
        # Send a POST request to the contactus view with the invalid form data
        response = self.client.post(reverse('contactus'), form_data)
        # Check if no ContactUs instance was created with the provided data
        self.assertEqual(ContactUs.objects.count(), 0)
        # Check if the form was re-rendered(redirected) with errors
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contactus'))


class ContactUsModelTest(TestCase):
    def test_send_response_mail_with_response(self):
        # Create a ContactUs instance with a response and an email address
        contact = ContactUs.objects.create(
            name='John Doe',
            email='shreyamishra414@gmail.com',
            query='Test query content.',
            response='Test response content.',
        )

        # response email should be sent because of pre_save

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check the email details
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, 'Response to your query')
        self.assertEqual(sent_email.from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(sent_email.to, ['shreyamishra414@gmail.com'])
        self.assertIn('Test response content.', sent_email.body)

    def test_send_response_mail_without_response(self):
        # Create a ContactUs instance without a response
        contact = ContactUs.objects.create(
            name='Jane Smith',
            email='shreyamishra414@gmail.com',
            query='Another test query.',
        )

        # Send the response email (should not send an email)
        contact.send_response_mail()

        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)
