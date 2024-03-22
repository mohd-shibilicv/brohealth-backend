from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.permissions import IsPatient
from patients.models import Patient
from patients.serializers import PatientSerializer


class ProtectedView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        return Response({"detail": "This is a protected view."}, status=200)


class PatientModelViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    permission_classes = [IsPatient]
    serializer_class = PatientSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
