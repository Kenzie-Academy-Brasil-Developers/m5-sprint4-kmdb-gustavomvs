from django.shortcuts import render
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate
from users.models import User
from users.permissions import AdmPermission
from users.serializers import LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RegisterView(APIView):

    def post(self, req):
        serializer = RegisterSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, 201)


class LoginView(APIView):
    def post(self, req):
        serializer = LoginSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data["email"], password=serializer.validated_data["password"])

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({"token": token.key})

        return Response({"detail" : "invalid email or password"}, 401)

class ListUsers(APIView):


    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, AdmPermission]

    def get(self, request):
        users = User.objects.all()
        serializer_response = RegisterSerializer(users, many=True)
        return Response(serializer_response.data)


class GetUser(APIView):


    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, AdmPermission]


    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer_response = RegisterSerializer(user)
            return Response(serializer_response.data)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, 404)
