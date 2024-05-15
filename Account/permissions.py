from rest_framework import permissions

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow students to edit their own details.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow students to edit their own details
        return request.user.is_authenticated and request.user.is_student

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers to edit their own details.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow teachers to edit their own details
        return request.user.is_authenticated and request.user.is_teacher

class IsSalesOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sales users to edit their own details.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow sales users to edit their own details
        return request.user.is_authenticated and request.user.is_sales
    


class IsWebAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sales users to edit their own details.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow sales users to edit their own details
        return request.user.is_authenticated and request.user.isWebAdmin
