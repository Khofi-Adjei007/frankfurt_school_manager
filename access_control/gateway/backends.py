import logging
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        logger.debug(f"Attempting to authenticate user with email: {username}")
        try:
            user = User.objects.get(email=username)
            logger.debug(f"User found: {user}")
            if user.check_password(password):
                logger.debug("Password check passed")
                return user
            else:
                logger.debug("Password check failed")
        except User.DoesNotExist:
            logger.debug(f"No user found with email: {username}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None