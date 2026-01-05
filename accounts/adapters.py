from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

User = get_user_model()
ALLOWED_DOMAIN = "pilani.bits-pilani.ac.in"


class RestrictedDomainSocialAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email

        if not email or not email.endswith(f"@{ALLOWED_DOMAIN}"):
            raise PermissionDenied("Only BITS Pilani emails allowed.")

        try:
            existing_user = User.objects.get(email=email)
            sociallogin.connect(request, existing_user)
            return
        except User.DoesNotExist:
            sociallogin.user.username = email.split("@")[0]
