# messaging_app/chats/auth.py

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Optionally customize the token response (e.g., include user ID, email)
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View to issue JWT tokens with custom payload
    """
    serializer_class = CustomTokenObtainPairSerializer
