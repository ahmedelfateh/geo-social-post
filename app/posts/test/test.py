from test_plus.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from app.utils.test_helper import get_tokens
from app.users.tests.factories import UserFactory
from app.posts.models import Post
from app.posts.test.factories import PostFactory


class TestPostCreateRetrieve(TestCase):
    def setUp(self):
        self.url = "/api/v1/posts/"
        self.client = APIClient()
        self.user = UserFactory()
        self._post = PostFactory(user=self.user)
        token = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.data = {"body": "test post"}

    def test_create_post(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(len(Post.objects.all()), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRetrieveAllPosts(TestCase):
    def setUp(self):
        self.url = "/api/v1/posts/all/"
        self.client = APIClient()
        self.user = UserFactory()
        self._post_1 = PostFactory(user=self.user)
        self._post_2 = PostFactory()
        token = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_retrieve_all_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRetrievePatchDeletePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_other = APIClient()
        self.user = UserFactory()
        self.user_other = UserFactory()
        self._post = PostFactory(user=self.user)
        token = get_tokens(self.user)
        token_other = get_tokens(self.user_other)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.client_other.credentials(HTTP_AUTHORIZATION=f"Bearer {token_other}")
        self.url = f"/api/v1/posts/{self._post.id}/"
        self.data = {"body": "test post"}

    def test_retrieve_post_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post_other_user(self):
        response = self.client_other.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_post_user(self):
        response = self.client.patch(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_post_other_user(self):
        response = self.client_other.patch(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_other_user(self):
        response = self.client_other.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestLikeUnlikePost(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_other = UserFactory()
        self.user = UserFactory()
        self._post = PostFactory(user=self.user_other)
        token = get_tokens(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.url_like = f"/api/v1/posts/{self._post.id}/like/"
        self.url_unlike = f"/api/v1/posts/{self._post.id}/unlike/"

    def test_like_post(self):
        response = self.client.post(self.url_like)
        self.assertEqual(response.data.get("like_count"), 1)
        self.assertEqual(response.data.get("unlike_count"), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_post(self):
        response = self.client.post(self.url_unlike)
        self.assertEqual(response.data.get("like_count"), 0)
        self.assertEqual(response.data.get("unlike_count"), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_unliked_post(self):
        self._post = PostFactory(user=self.user, unlike=[self.user.id])
        self.assertEqual(self._post.like_count, 0)
        self.assertEqual(self._post.unlike_count, 1)

        response = self.client.post(self.url_like)
        self.assertEqual(response.data.get("like_count"), 1)
        self.assertEqual(response.data.get("unlike_count"), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_liked_post(self):
        self._post = PostFactory(user=self.user, like=[self.user.id])
        self.assertEqual(self._post.like_count, 1)
        self.assertEqual(self._post.unlike_count, 0)

        response = self.client.post(self.url_unlike)
        self.assertEqual(response.data.get("like_count"), 0)
        self.assertEqual(response.data.get("unlike_count"), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
