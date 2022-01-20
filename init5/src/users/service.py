from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))

def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))

def send(user_email, secret_code):
    send_mail(
        'Your registration',
        f'Your activation code: {secret_code}',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )