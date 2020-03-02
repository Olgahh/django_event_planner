from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
	message = "You must be an Organiser"

	def has_object_permission(self, request, view, obj):
		return obj.organizer == request.user
