from rest_framework import serializers
from AuthApp.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from fullAuthAPI.settings import EMAIL_HOST_USER


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(
                "Password and Password2 doesn't matched")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'created_at']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Your password doesn't macth")
        user.set_password(password)
        user.save()
        return attrs

# Email for confirm password reset link


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            u = User.objects.filter(email=email)
            user = User.objects.get(email=email)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            print("User id ", user_id)
            token = PasswordResetTokenGenerator().make_token(user)
            print("User token ", token)
            link = "http://127.0.0.1:8000/password-reset-link/"+user_id+'/'+token
            print('Link', link)

            # send email configuration
            subject = 'Password Reset'
            message = f"Your password reset link: {link}"
            from_email = EMAIL_HOST_USER
            to_email = email
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
            )

        else:
            raise serializers.ValidationError('Your email is not valid')
        return attrs


class PasswordResetEmailLinkSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user_id = self.context.get('user_id')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError(
                'Your password and password2 is not same')
        user_id = smart_str(urlsafe_base64_decode(user_id))
        user = User.objects.get(id=user_id)
        if PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
        return attrs
