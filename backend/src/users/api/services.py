from users.models import User


def is_user_exists(user_id):
    return User.objects.filter(id=user_id).exists()
