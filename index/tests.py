from django.test import TestCase, override_settings
from social_django.compat import reverse

@override_settings(SOCIAL_AUTH_GITHUB_KEY = '1', SOCIAL_AUTH_GITHUB_SECRET='2')
class AuthTestcase(TestCase):

    def setUp(self):
        session = self.client.session
        session["github_status"] = "1"
        session.save()

    def test_begin_view(self):
        response = self.client.get(reverse('social:begin', kwargs={'backend': 'github'}))
        self.assertEqual(response.status_code, 302)
