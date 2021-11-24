from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from .models import UserProfile

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_profile = UserProfile.objects.get(username__username = user.username)
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user_profile.email_verified)
        +six.text_type(user.email))

generate_token = TokenGenerator()
