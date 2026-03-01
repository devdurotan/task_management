from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime


class JWTService:
    """
    Customised JWT token generation 
    """

    @staticmethod
    def generate_tokens(user):
        """
        Generate access & refresh tokens for a user
        """
        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "access_token_exp": datetime.fromtimestamp(
                refresh.access_token["exp"]
            ),
            "refresh_token_exp": datetime.fromtimestamp(
                refresh["exp"]
            ),
        }