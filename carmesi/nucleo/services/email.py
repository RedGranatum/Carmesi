
# DJANGO
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Utilities

# Services
from users.services import user_create
from nucleo.services.token import token_verification

def email_send_confirmation_preclient(email, owner_name):
    """ Send account verification link """
    verification_token = token_verification(email, owner_name)

    subject = 'Hola {} Para continuar con tu registro en Redgranatum, verifica tu email'.format(owner_name)
    from_email = 'administrador@redgranatum.com'
    content = render_to_string(
        'emails/users/account_verificaction.html',
        {'token': verification_token, 'email': email}
    )

    msg = EmailMultiAlternatives(subject, content, from_email, [email])
    msg.attach_alternative(content, "text/html")
    msg.send()

    print("Enviando email")

