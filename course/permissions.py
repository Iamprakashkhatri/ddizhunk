from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()


# class IsTeacher(BasePermission):
	
#     def has_object_permission(self, request, view, obj):
#         return bool(request.user.is_teacher)

class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_teacher)

