from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied

ALLOWED_DOMAIN = "pilani.bits-pilani.ac.in"


class RestrictedDomainAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if not email.endswith(f"@{ALLOWED_DOMAIN}"):
            raise PermissionDenied("Only BITS Pilani emails allowed.")
        return email


class RestrictedDomainSocialAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        if not email or not email.endswith(f"@{ALLOWED_DOMAIN}"):
            raise PermissionDenied("Only BITS Pilani emails allowed.")
