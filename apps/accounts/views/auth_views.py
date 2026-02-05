from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import redirect
from allauth.socialaccount.providers.discord.views import DiscordOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView

from accounts.services.auth_service import AuthService

class DiscordLoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # if not user.is_authenticated:
        #     return redirect(settings.FRONTEND_LOGIN_URL)
        tokens = AuthService.generate_jwt(user)
        frontend_url = settings.FRONTEND_CALLBACK_URL
        redirect_url = (f"{frontend_url}?access={tokens['access']}&refresh={tokens['refresh']}")
        return redirect(redirect_url)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=400)
        
        try:
            AuthService.logout(refresh_token)
            return Response({"message": "Successfully logged out."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
class DiscordLoginRedirectView(OAuth2LoginView):
    adapter_class = DiscordOAuth2Adapter
    client_class = OAuth2Client

discord_login = DiscordLoginRedirectView.as_view()