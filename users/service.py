import os
from random import randint
from datetime import timedelta

from django.db import transaction
from django.core.mail import send_mail
from django.utils import timezone

from .models import CustomUser, UserOTP
from .tasks import send_otp_email


class UserService:

    @staticmethod
    def generate_otp():
        return randint(100000, 999999)

    @staticmethod
    def send_otp_email(username, email, otp):
        send_mail(
            subject="Verify your OTP!",
            message=f"Hello {username}, Your OTP: {otp}",
            html_message=f"""
                <p>Hello <strong>{username}</strong></p>
                <p>Your OTP is: <strong>{otp}</strong></p>
            """,
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

        UserOTP.objects.create(
            user=user,
            otp=str(otp)
        )

        transaction.on_commit(
            lambda: send_otp_email.delay(
                user.username,
                user.email,
                str(otp)
            )
        )

        return user

    @staticmethod
    @transaction.atomic
    def verify_otp(otp: str):

        try:
            obj_otp = UserOTP.objects.select_for_update().get(
                otp=otp,
                is_used=False,
            )

        except UserOTP.DoesNotExist:
            return False

        if obj_otp.created_at < timezone.now() - timedelta(minutes=5):
            return False

        user = obj_otp.user

        obj_otp.is_used = True
        obj_otp.save(update_fields=["is_used"])

        user.is_active = True
        user.save(update_fields=["is_active"])

        return True