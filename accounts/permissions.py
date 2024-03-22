from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    Custom permission to only allow patients to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is a patient
        return request.user.role == 'patient'

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsDoctor(permissions.BasePermission):
    """
    Custom Permission to only allow docotrs to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if the user is a doctor
        return request.user.role == 'doctor'
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(permissions.BasePermission):
    """
    Custom Permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if the user is a admin
        return request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
