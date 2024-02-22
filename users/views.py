from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()  # Kullanıcı nesnesi kaydedilir.
        refresh = RefreshToken.for_user(user)  # Yeni kullanıcı için JWT tokenları üretilir.
        
        # Yanıt verilerine tokenları ekleyin.
        serializer.validated_data["refresh"] = str(refresh)
        serializer.validated_data["access"] = str(refresh.access_token)