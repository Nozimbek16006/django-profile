import os
from django.db import transaction
from .models import CustomUser, UserOTP
from random import randint
from django.core.mail import send_mail
from .tasks import send_otp_email
from datetime import timedelta
from django.utils import timezone


class UserService:
    @staticmethod
    def generate_otp():
        return randint(100000, 999999)

    @staticmethod
    def send_otp_email(username: str, email: str, otp: str):
        send_mail(
            subject="Verify your OTP!",
            message=f"Hello Dear {username} Your OTP: {otp}",
            html_message=f"<p>Hello Dear <strong>{username}</strong>, Your OTP is <strong>{otp}</strong></p>",
            from_email=os.getenv("FROM_EMAIL"),
            recipient_list=[email],
        )

    @staticmethod
    @transaction.atomic
    def create_user(username, email, password):
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
        )
        otp = UserService.generate_otp()
        UserOTP.objects.check(user=user, otp=otp)

        transaction.on_commit(lambda: send_otp_email.delay(user.username, user.email, str(otp)))

    @staticmethod
    @transaction.atomic
    def verify_user(otp: str):
        try:
            obj_otp = UserOTP.objects.select_for_update().get(
                otp=otp,
                is_used=False,
            )
        except UserOTP.DoesNotExist:
            return False
        if obj_otp.created_at < timezone.localtime(timezone.now() - timedelta(minutes=5)):
            return False
        obj_otp.is_used = True
        obj_otp.save(update_fields=['is_used'])
        obj_otp.is_active = True
        obj_otp.user.save(update_fields=['is_active'])
        return True