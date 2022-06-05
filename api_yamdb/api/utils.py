import random
import string
from django.http import Http404
from django.core.mail import send_mail
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, Http404):
        response.data['detail'] = exc.args[0]
    return response


def send_email(email, code):
    mail_subject = 'Код подтверждения'
    message = (f'Ваш код подтверждения: {code} . ')
    send_mail(mail_subject, message, 'artemslaks@gmail.com',
              [email], fail_silently=False)


def code_gen():
    generate_code = ''.join(random.choices(string.digits, k=6))
    return(int(generate_code))


print(send_email('pavelmyskin22@gmail.com', code_gen()))
