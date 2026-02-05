from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:
    @staticmethod
    def generate_jwt(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    @staticmethod
    def logout(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise e