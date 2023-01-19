from django.core.mail import send_mail


def confirmation_code_email(email, confirmation_code):
    """Шаблон письма для отправки пользователю кода подтверждения."""

    email_subject = "Код подтверждения для регистрации на YaMDB"
    email_body = (f"Вы запросили 'код подтверждения' для получения токета "
                  f"YaMDB.\n\nВнимание, храните его в тайне.\n"
                  f"Ваш код подтверждения: {confirmation_code}")
    send_mail(
        email_subject,
        email_body,
        'no-reply@yamdb.com',
        [email],
        fail_silently=False
    )
