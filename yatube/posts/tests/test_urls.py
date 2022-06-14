from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-decsr',
        )
        cls.user = User.objects.create_user(username='Test_user')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            pk='1234',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client(self.user)
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        """Страница /create/ доступна авторизованому."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        page_status = {'/create/': HTTPStatus.OK}
        for page, status in page_status.items():
            with self.subTest(page=page, status=status):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, status)

    def test_urls_exists_at_desired_location(self):
        """Проверка страниц на доступность."""
        static_urls = {
            '/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            '/group/test-slug/': HTTPStatus.OK,
            '/profile/Test_user/': HTTPStatus.OK,
            '/posts/1234/': HTTPStatus.OK,
            '/posts/1234/edit/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
            # '/posts/1234/create/': HTTPStatus.OK,
        }
        for address, response_on_url in static_urls.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, response_on_url)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/create/': 'posts/create.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/Test_user/': 'posts/profile.html',
            '/posts/1234/': 'posts/post_detail.html',
            '/posts/1234/edit/': 'posts/create.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
