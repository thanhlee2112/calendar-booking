from accounts.views.auth_views import DiscordLoginView, LogoutView, DiscordLoginRedirectView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/discord/success', DiscordLoginView.as_view(), name='discord-login'),
    path('auth/logout/', LogoutView.as_view(), name='discord-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]