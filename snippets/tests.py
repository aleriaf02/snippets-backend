import json
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from snippets.models import Snippet, File, Comment
from snippets.serializers import SnippetSerializer
from topics.models import Topic

User = get_user_model()


class AuthAPITestCase(APITestCase):
    def setUp(self):
        user = User(email='testuser@snip.com', username='test_user')
        user.set_password('test_pass')
        user.save()
        self.user = user

        response = self.client.post(
            '/api/auth/login/', {
                'username': 'test_user',
                'password': 'test_pass',
            },
            format='json'
        )
        result = json.loads(response.content)
        self.access_token = result['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)


class SnippetListTestCase(AuthAPITestCase):
    url = reverse("snippets:snippet-list")

    def setUp(self):
        super().setUp()
        self.mock_data()

    def mock_data(self):
        Topic.objects.create(id=0, name='JS')
        Topic.objects.create(id=1, name='TEST')
        self.snippet = {
            'name': 'Test Snippet',
            'description': 'Test snippet description',
            'files': [
                {
                    'name': 'test_file1.py',
                    'content': 'console.log("test1")'
                },
                {
                    'name': 'test_file2.py',
                    'content': 'console.log("test2")'
                },
                {
                    'content': 'console.log("test3")',
                    'name': 'test_file3.py'
                }
            ],
            'topic_ids': [0, 1]
        }

    # TESTS
    def test_create_snippet(self):
        """Verify snippet creation"""

        snippet = self.snippet
        response = self.client.post(
            self.url, snippet,
            format='json'
        )
        result = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertEqual(snippet['name'], result['name'])
        self.assertEqual(snippet['description'], result['description'])
        self.assertCountEqual(snippet['topic_ids'], list(map(lambda topic: topic['id'], result['topics'])))
        for file in result['files']:
            file.pop('id')
        self.assertCountEqual(snippet['files'], result['files'])

    def test_list_snippets_pagination(self):
        """Verify snippet list pagination"""

        for i in range(0, 20):
            self.client.post(self.url, self.snippet, format='json')
        response = self.client.get(self.url, format='json')
        result = json.loads(response.content)

        self.assertEqual(result['count'], 20)
        self.assertIsNotNone(result['next'])
        self.assertIsNone(result['previous'])


class SnippetDetailTestCase(AuthAPITestCase):

    def setUp(self):
        super().setUp()
        self.mock_data()
        self.url = reverse("snippets:snippet-detail", kwargs={"pk": self.snippet.pk})

    def mock_data(self):
        self.snippet = Snippet.objects.create(user=self.user, name='Test Snippet',
                                              description='Test snippet description')
        self.snippet.topics.set([Topic.objects.create(id=0, name='JS'),
                                 Topic.objects.create(id=1, name='TEST')])
        self.snippet.files.set([
            File.objects.create(snippet=self.snippet, name='test_file1.py', content='console.log("test1")'),
            File.objects.create(snippet=self.snippet, name='test_file2.py', content='console.log("test2")'),
            File.objects.create(snippet=self.snippet, name='test_file3.py', content='console.log("test3")'),
        ])
        self.snippet.save()

    # TESTS
    def test_snippet_object_bundle(self):
        """
        Verify snippet object bundle
        """

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        serializer_data = SnippetSerializer(instance=self.snippet).data
        response_data = json.loads(response.content)
        self.assertEqual(serializer_data, response_data)


class SnippetCommentsTestCase(AuthAPITestCase):

    def setUp(self):
        super().setUp()
        self.mock_data()
        self.url = reverse("snippets:snippet-comments-list", kwargs={"snippet_id": self.snippet.pk})

    def mock_data(self):
        self.snippet = Snippet.objects.create(user=self.user, name='Test Snippet',
                                              description='Test snippet description')
        self.snippet.comments.set([
            Comment.objects.create(snippet=self.snippet, user=self.user, content='Test comment 1', id=1),
            Comment.objects.create(snippet=self.snippet, user=self.user, content='Test reply 1', id=2, parent_id=1),
            Comment.objects.create(snippet=self.snippet, user=self.user, content='Test reply 2', id=3, parent_id=1),
        ])
        self.snippet.save()

        self.comment = {
            'content': 'Test comment 4',
        }

    def test_create_snippet_comment(self):
        """
        Verify top level snippet comment creation
        """

        comment = self.comment
        response = self.client.post(
            self.url, comment,
            format='json'
        )
        result = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertEqual(comment['content'], result['content'])
        self.assertEqual(None, result['parent'])

    def test_create_snippet_comment_reply(self):
        """
        Verify snippet comment reply
        """

        # Test valid reply creation
        comment = self.comment
        comment['parent'] = 1
        response = self.client.post(
            self.url, comment,
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(201, response.status_code)
        self.assertEqual(comment['content'], result['content'])
        self.assertEqual(comment['parent'], result['parent'])

        # Test invalid reply creation (nested)
        comment['parent'] = result['id']
        response = self.client.post(
            self.url, comment,
            format='json'
        )
        self.assertEqual(400, response.status_code)

    def test_snippet_comment_object_bundle(self):
        """
        Verify snippet comment object bundle
        """

        response = self.client.get(self.url, format='json')
        result = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(result['count'], 1)
        comment = result['results'][0]
        self.assertEqual(len(comment['replies']), 2)