from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        """Create test client, add new user, make sure user is logged in
            Create regular user
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@fii-na.com",
            password="test123"
        )
        # log a user in with django authentication
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test2@fii-na.com",
            password="test123",
            name='Test USER full name'
        )

    def test_users_listed(self):
        """test users are listed on user page with custom django admin"""
        # can be found in django admin documentation
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # django custom assertion that check response contains certain items
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that a user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test creat user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
