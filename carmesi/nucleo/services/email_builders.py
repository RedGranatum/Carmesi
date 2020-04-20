# DJANGO
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Services & Builder
from nucleo.services.token_builders import TokenFactory


_tokenFactory = TokenFactory()


class EmailBase(object):
    """ Clase base para la creacion de emails """
    def __init__(self):
        self.set_from_email()
        self.email = None
        self.subject = None
        self.content = None
        self.template = None
        self.token = None
        self.body = {}
        self.token_builder = None

    def set_from_email(self):
        self.from_email = 'administrador@redgranatum.com'

    def set_template(self, template):
        self.template = template

    def set_email(self, email):
        self.email = email

    def set_name(self, name):
        self.name = name

    def set_content(self):
        self.content= render_to_string(self.template, {'token': self.token, 'email': self.email} )

    def set_token(self, token):
        self.token = token

    def get_body(self):
        self.body = {'email': self.email, 'name': self.name,
                     'subject': self.subject, 'content': self.content}
        return self.body

    def set_token_builder(self, token_builder):
        self.token_builder = token_builder

    def get_token_payload(self):
        return {}

    def build_token(self):
        data = self.get_token_payload()
        token_obj = self.token_builder(data)
        self.token = token_obj.get_jwt()


    def enviar(self):
        self.set_content()
        msg = EmailMultiAlternatives(self.subject, self.content, self.from_email, [self.email])
        msg.attach_alternative(self.content, "text/html")
        msg.send()

    def __str__(self):
        return 'From:{} To {} Subject {}'.format(
            self.from_email, self.email, self.subject)


class EmailClienteBuilder(EmailBase):
    def __init__(self):
        super().__init__()
        self.set_template('emails/client_verification.html')
        self.set_token_builder(_tokenFactory.crear_token_cliente)

    def set_subject(self):
        self.subject = f'Hola {self.name} Para continuar con tu registro en Carmesi, verifica tu email'

    def get_token_payload(self):
        data = {'email':self.email, 'owner_name':self.name}
        return data


class EmailUsuarioBuilder(EmailBase):
    def __init__(self):
        super().__init__()
        self.set_template('emails/user_verification.html')
        self.set_token_builder(_tokenFactory.crear_token_usuario)

    def set_subject(self):
        self.subject = f'Hola {self.name} Para continuar con tu registro en Carmesi como usuario de, verifica tu email.'

    def get_token_payload(self):
        data = {'email':self.email, 'name':self.name}
        return data

class EmailBuilder(object):

    def crear_de_tipo_cliente(self, email, name):
        self.builder = EmailClienteBuilder()
        self.builder.set_email(email)
        self.builder.set_name(name)
        self.builder.set_subject()
        self.builder.set_content()
        return self.builder

    def crear_de_tipo_usuario(self, email, name):
        self.builder = EmailUsuarioBuilder()
        self.builder.set_email(email)
        self.builder.set_name(name)
        self.builder.set_subject()
        self.builder.set_content()
        return self.builder
