import re, os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validar_cpf(value):
    cpf = re.sub(r'\D', '', value)  # Remove pontos, traço e espaços

    if len(cpf) != 11:
        raise ValidationError('O CPF deve conter exatamente 11 números.')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido (dígitos repetidos).')

    # Primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        raise ValidationError('CPF inválido.')

    # Segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf[10]):
        raise ValidationError('CPF inválido.')

def validar_telefone(value):   
    telefone_validator = RegexValidator(
        regex=r'^\d{2}\s\d{9}$',
        message="Telefone deve estar no formato: 11 912345678 (2 dígitos DDD, espaço, 9 dígitos do número)."
    )
    telefone_validator(value)

def validar_rg(value):
    # Remove qualquer ponto ou traço (caso tenha sido informado nesse formato)
    value = re.sub(r'[^\d]', '', value)
    
    if not re.match(r'^\d{11}$', value):
        raise ValidationError('O RG deve conter 11 dígitos numéricos.')

    return value

def validar_ingressao(value):
    ingressao_validator = RegexValidator(
        regex=r'^\d{4}\.\d{1}$',
        message="Digite um ano seguido do semestre de ingressão, Exemplo: 2023.2"
    )
    try:
        ingressao_validator(value)
    except ValidationError as e:
        raise e

def validar_arquivo(arquivo):
    extensoes_permitidas = ['.pdf', '.jpg', '.jpeg', '.png']
    tamanho_maximo = 10 * 1024 * 1024  # 10MB

    ext = os.path.splitext(arquivo.name)[1].lower()
    if ext not in extensoes_permitidas:
        raise ValidationError('Tipo de arquivo não permitido. Envie um PDF ou imagem (JPG, PNG).')

    if arquivo.size > tamanho_maximo:
        raise ValidationError('O arquivo excede o tamanho máximo de 10MB.')

def validar_termo(value):
    if value == False:
        raise ValidationError('Você deve aceitar os termos de inscrição para prosseguir')