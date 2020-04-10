
# Django

# Models Serializers
from users.models import User


def user_create(
    *,
    email: str,
    first_name: str,
    last_name: str,
    password: str
) -> User:
    user = User(username=email, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.full_clean()
    user.save()

    return user
