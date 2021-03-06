from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def create_confirm_payloads(user):
    uid = encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    return uid, token


def send(user_email, subject, html_message):
    send_mail(
        subject=subject,
        message=None,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
        html_message=html_message
    )
