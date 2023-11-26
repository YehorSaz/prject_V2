import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from configs.celery import app

from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_NAME'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def email_to_admin(cls, data):
        cls.__send_email.delay(os.environ.get('ADMIN_EMAIL'), 'email_to_admin.html', {'post_id': data}, 'check this post')

    @classmethod
    def missing_car(cls, data):
        cls.__send_email.delay(os.environ.get('ADMIN_EMAIL'), 'missing_car.html', {'message': data['message']},
                         f'Email from user: {data["user"]}, user_id: {data["user_id"]}')

    @classmethod
    def register_email(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(
            user.email,
            'register.html',
            {'name': user.profile.name, 'url': url},
            'Register'
        )

    @classmethod
    def recovery_email(cls, user):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email.delay(user.email, 'recovery.html', {'url': url}, 'Recovery password')


