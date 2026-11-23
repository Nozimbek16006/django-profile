from celery import shared_task

@shared_task
def send_otp_email(username: str, email: str, otp: str):
    from users.service import UserService
    UserService.send_otp_email(username, email, otp)
    return f"OTP was sent to {email}"