def role_checks(request):
    """
    Context processor to add is_teacher and is_student flags to all templates.
    This avoids the OneToOneField DoesNotExist exception in templates.
    """
    if not request.user.is_authenticated:
        return {}
    
    return {
        'is_teacher': hasattr(request.user, 'teacher'),
        'is_student': hasattr(request.user, 'student'),
        'is_superuser': request.user.is_superuser,
    }
