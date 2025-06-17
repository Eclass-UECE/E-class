from django.http import HttpResponse

from django.core.mail import send_mail

send_mail(
    'Assunto de Teste',
    'Corpo do e-mail de teste',
    'joaopedrollnet@gmail.com',  # De
    ['joaopedrollnet@gmail.com'],  # Para
    fail_silently=False,
)
