def format_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'uuid':  str(user.uuid),
        'last_name': user.last_name,
        'is_active': user.is_active,
        'is_staff': user.is_staff
    }
