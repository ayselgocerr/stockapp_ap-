# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password

# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from rest_framework.authtoken.models import Token
# from dj_rest_auth.serializers import TokenSerializer




# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
#     password = serializers.CharField(write_only=True, validators=[validate_password])
#     password2 = serializers.CharField(required=True,write_only=True, validators=[validate_password])

#     token = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             "id",  # read_only
#             "email",
#             "username",
#             "first_name",
#             "last_name",
#             "password",  # write_only
#             "password2",  # write_only
#             "token",
#         )

#     def get_token(self, user_object):
#         token = Token.objects.get(user=user_object)
#         return token.key


#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError({
#                 "message": "Password fields didn't match!!"
#             })
        
#         return data

#     def create(self, validated_data):
#         validated_data.pop('password2')
#         password = validated_data.pop('password')
#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

#         # set_password = set_password(validated_data['password'])
#         # user = User.objects.create(
#         #     fist_name = validated_data['first_name'],
#         #     last_name = validated_data['last_name'],
#         #     email = validated_data['email'],
#         #     username = validated_data['username'],
#         #     password = set_password
#         # )
#         # return user
    
# class UserTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "first_name", "last_name", "email", "username")

# class CustomTokenSerializer(TokenSerializer):
#     user = UserTokenSerializer(read_only=True)
    
#     class Meta:
#         model = Token
#         fields = ("key", "user")
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username
        return token