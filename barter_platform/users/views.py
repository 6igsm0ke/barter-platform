from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions, viewsets, decorators


# Create your views here.

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self,request, *args, **kwargs):
        # Кастомные ошибки
        errors = {
            "001": "Email is already in use",
            "002": "Email is required",
            "003": "Password is required",
            "004": "Invalid date format",
            "005": "Serilizer error",
            "999": "Something went wrong",
        }
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if (not serializer.is_valid()):
                code = '005'
                return Response(
                    {"error": errors[code], "description": serializer.errors, "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            email = data.get("email")
            password = data.get("password")
            if User.objects.filter(email=email, is_active=True).exists():
                code = "001"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not email:
                code = "002"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not password:
                code = "003"
                return Response(
                    {"error": errors[code], "code": code},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Можно использовать для очистки неактивных пользователей но пока не нужно 
            User.objects.filter(email=email, is_active=True).delete() # Пока is_active = True можно сделать False в будущем потребуется внедрить систему верификации 
            user = serializer.save()

            return Response(
                {"message": "User created successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            code = "999"
            return Response(
                {"error": errors[code], "code": code},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    @decorators.action(detail=False, methods=["get"], permission_classes=permission_classes)
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)