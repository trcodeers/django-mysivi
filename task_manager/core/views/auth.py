from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from core.models import User, Company
from core.serializers.auth import ManagerSignupSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.authentication import CsrfExemptSessionAuthentication
from core.throttles import LoginRateThrottle, SignupRateThrottle, TaskCreateRateThrottle

class ManagerSignupAPIView(APIView):
    throttle_classes = [SignupRateThrottle]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ManagerSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create or get company
        company, _ = Company.objects.get_or_create(
            name=serializer.validated_data["company_name"]
        )

        # Create manager
        manager = User.objects.create(
            username=serializer.validated_data["username"],
            role="MANAGER",
            company=company
        )
        manager.set_password(serializer.validated_data["password"])
        manager.save()

        return Response(
            {
                "manager_id": manager.id,
                "company_id": company.id,
                "message": "Manager created successfully",
            },
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(APIView):
    throttle_classes = [LoginRateThrottle]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        #  creates session (Django handles cookie)
        login(request, user)

        return Response(
            {"message": "Login successful"},
            status=status.HTTP_200_OK
        )

class LogoutAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "role": request.user.role
        })

# For testing free access without authentication
class FreeResourceAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"message": "This is a free resource accessible without authentication."})