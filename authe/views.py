from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from authe.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from authe.serializers import LoginSerializer, RegisterSerializer
from drf_yasg import openapi


@swagger_auto_schema(
    method="get",
    tags=["Auth"]
)
@api_view(['GET'])
def me_view(request):
    return Response({"username": request.user.username, "user_id": request.user.id,  "role": request.user.role})

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, example='Joanna'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, example='my7bestie'),
        },
    ),
    operation_summary="Register new student",
    responses={201: "Created", 400: "Validation error"},
    tags=["Auth"]
)
@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    operation_summary="Login and get access/refresh tokens",
    responses={200: "Success", 400: "Bad request", 404: "User not found"},
    tags=["Auth"]
)
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    user = User.objects.filter(username=username).first()
    if not user:
        return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, user.password):
        return Response({"error": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    access_token['role'] = user.role

    return Response({"access_token": str(access_token), "refresh_token": str(refresh)})