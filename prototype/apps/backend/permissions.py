from rest_framework import permissions

class PersonPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow people to modify their own profiles.
        return request.method in permissions.SAFE_METHODS or obj.user == request.user

class CandidateSkillPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow people to modify their own profiles.
        return request.method in permissions.SAFE_METHODS or obj.candidate.user == request.user

class CandidateDocPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow people to modify their own documents.
        return request.method in permissions.SAFE_METHODS or obj.candidate.user == request.user

class JobPostPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow the employer who created a JobPost to modify or delete it.
        return request.method in permissions.SAFE_METHODS or obj.contact_person.user == request.user

class JobSkillPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow the employer who created a JobPost to modify the skill requirements.
        return request.method in permissions.SAFE_METHODS or obj.job.contact_person.user == request.user
