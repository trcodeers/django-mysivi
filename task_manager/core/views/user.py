from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers.user import ReporteeCreateSerializer
from core.permissions import IsManager
from core.authentication import CsrfExemptSessionAuthentication


class CreateReporteeAPIView(APIView):
    """
        ONLY Manager can create reportees
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = ReporteeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        manager = request.user  # 🔥 THIS IS NOW SAFE & CORRECT

        reportee = User.objects.create(
            username=serializer.validated_data["username"],
            role="REPORTEE",
            company=manager.company,
            manager=manager
        )
        reportee.set_password(serializer.validated_data["password"])
        reportee.save()

        return Response(
            {
                "id": reportee.id,
                "username": reportee.username,
                "message": "Reportee created successfully",
            },
            status=status.HTTP_201_CREATED
        )
