from rest_framework import permissions

class HasVideoAccess(permissions.BasePermission):
    """
    Custom permission to check if a user can access a specific video(paid videos).
    """
    message = "You need to purchase this course to watch or download this video."

    def has_object_permission(self, request, view, obj):
        # obj is the instance of the Videos model
        
        # If the video is free or the entire course is free, allow access
        if obj.is_free or obj.course.is_free:
            return True
            
        # If it's a paid video, the user must be authenticated (logged in)
        if not request.user or not request.user.is_authenticated:
            return False
            
        # Check user has this course in purchased list
        # We use .exists() for better database performance instead of .all()
        if request.user.courses.filter(id=obj.course.id).exists():
            return True
            
        return False