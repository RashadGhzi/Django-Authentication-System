from django.shortcuts import render
from rest_framework.response import Response
from AuthApp.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from AuthApp.renderers import UserRenderers
from AuthApp.custom_token import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class UserRegistration(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer_data = UserSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            user = serializer_data.save()
            token = get_tokens_for_user(user)
            return Response({'msg': 'data has created', 'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer_data = UserLoginSerializer(data=request.data)

        if serializer_data.is_valid(raise_exception=True):
            email = serializer_data.data.get('email')
            password = serializer_data.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'successfully logeIn', 'token': token}, status=status.HTTP_200_OK)
            return Response({'error': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProifile(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer_data = UserProfileSerializer(request.user)
        return Response({'data': serializer_data.data}, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    renderer_classes = [UserRenderers]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer_data = ChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializer_data.is_valid(raise_exception=True):
            return Response({'msg': 'password has updated'}, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmail(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer_data = SendPasswordResetEmailSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            return Response({'msg': 'Password reset link has send to your email'}, status=status.HTTP_201_CREATED)


class PasswordResetEmailLink(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, userid, token, format=None):
        serializer_data = PasswordResetEmailLinkSerializer(
            data=request.data, context={'user_id': userid, 'token': token})
        if serializer_data.is_valid(raise_exception=True):
            return Response({'msg': 'your password has been updated'})
