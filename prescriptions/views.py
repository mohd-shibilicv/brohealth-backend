from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from prescriptions.models import Prescription
from prescriptions.serializers import PrescriptionSerializer, CreatePrescriptionSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):
        appointment_id = self.request.query_params.get('appointmentId')
        if appointment_id:
            queryset = Prescription.objects.filter(appointment=appointment_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        limit = self.request.query_params.get('limit')
        user = self.request.user
        if user.role:
            if user.role == "doctor":
                if limit:
                    return Prescription.objects.filter(doctor__user=user)[:int(limit)]
                return Prescription.objects.filter(doctor__user=user)
            elif user.role == "patient":
                if limit:
                    return Prescription.objects.filter(doctor__user=user)[:int(limit)]
                return Prescription.objects.filter(patient__user=user)
        return Prescription.objects.all()


class CreatePrescriptionView(APIView):
    def post(self, request):
        serializer = CreatePrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            prescription_image = request.FILES.get('prescription_image')
            if prescription_image:
                serializer.save(prescription_image=prescription_image)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
