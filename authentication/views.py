from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema_view(
    post=extend_schema(description='Registers a user and returns an access and refresh JSON web token pair.'),
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GoogleLogin(SocialLoginView):
    """
    Exchanges Google's access code for an access_token.
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class GithubLogin(SocialLoginView):
    """
    Exchanges GitHub's access code for an access_token.
    """

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
