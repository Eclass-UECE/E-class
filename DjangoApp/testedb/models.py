from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .validators import validar_cpf, validar_telefone, validar_rg, validar_ingressao

# Choices
turnos_escolhas = [
    ('Matutino', 'Matutino'),
    ('Vespertino', 'Vespertino'),
    ('Noturno', 'Noturno'),
]

aluno_uece_escolhas = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Outro', 'Outro')
]

turma_entrada_escolhas = [
    ('Manhã', 'S01 - Turma A: sábado, manhã 08h às 11h40.'),
    ('Tarde', 'S01 - Turma B: sábado, tarde 13h às 16h40.')
]

termo_escolhas = [
    ('Sim', 'Sim'),
    ('Não', 'Não')
]

como_conheceu_escolhas = [
    ('Rede_Social', 'Rede Social'),
    ('Indicação', 'Indicação'),
    ('TV', 'TV'),
    ('Outro', 'Outro')
]

tipo_prova_escolhas = [
    ('Writing', 'Writing'),
    ('Use_of_english', 'Use of english'),
    ('Speaking', 'Speaking'),
    ('Listening', 'Listening')
]

priodades_escolhas = [
    ('Aluno_UECE', 'Aluno de Letras-Inglês da UECE'),
    ('Prof_Ingles', 'Atua como professor de inglês na rede pública'),
    ('Aluno_Egresso', 'Aluno egresso do curso de Letras-Inglês'),
    ('Prof_Publi', 'Professor da rede pública'),
    ('Pesquisador', 'Atua como pesquisador'),
    ('Pos_grad', 'Cursa pós-graduação'),
    ('Graduacao', 'Cursa graduação'),
    ('Aluno_subsequente', 'Aluno de curso técnico/subsequente'),
    ('Ex_aluno_reprovado', 'Ex aluno do E-class (Reprovado)'),
    ('Ex_aluno_desistente', 'Ex aluno do E-class (Desistente)'),
    ('Servidor_UECE', 'Servidor da UECE'),
    ('Servidor_publi', 'Servidor público'),
    ('Nenhum', 'Não me enquadro em nenhuma das anteriores')
]


class Turmas(models.Model):
    id = models.AutoField(_('ID_Turma'), primary_key=True)
    semestre_letivo = models.CharField(_('Semestre da turma'), max_length=6, validators=[validar_ingressao], null=False)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20, null=False)
    sala = models.CharField(_('Sala'), max_length=10, null=False)
    num_vagas = models.PositiveIntegerField(_('Vagas'), null=False)

    def __str__(self):
        return f"Turma {self.id} - {self.semestre_letivo}"

class Alunos(models.Model):
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=11, primary_key=True, validators=[validar_cpf])
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    email = models.EmailField(_('Email'), null=False)
    instituicao_ensino = models.CharField(_('Instituição de ensino'), max_length=255, null=False)
    ocupacao = models.CharField(_('Ocupação'), max_length=255, null=False)
    semestre = models.PositiveIntegerField(_('Semestre'), validators=[MinValueValidator(1), MaxValueValidator(6)], null=False)
    relatorio = models.TextField(_('Relatório'), null=True, blank=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_completo

class Professores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=11, unique=True, validators=[validar_cpf], null=False)
    rg = models.CharField(_('RG'), max_length=9, unique=True, validators=[validar_rg], null=False)
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    email = models.EmailField(_('Email'), null=False)
    endereco = models.CharField(_('Endereço'), max_length=255, null=False)
    semestre_ingressao = models.CharField(_('Semestre de Ingresso'), max_length=6, validators=[validar_ingressao], null=False)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20, null=False)

    def __str__(self):
        return self.nome_completo

class Coordenadores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=11, unique=True, validators=[validar_cpf], null=False)
    rg = models.CharField(_('RG'), max_length=9, unique=True, validators=[validar_rg], null=False)
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    email = models.EmailField(_('Email'), null=False)

    def __str__(self):
        return self.nome_completo

class Inscricao(models.Model):
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=11, unique=True, validators=[validar_cpf], null=False)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    email = models.EmailField(_('Email'), null=False)
    telefone = models.CharField(_('Telefone (WhatsApp)'), max_length=12, validators=[validar_telefone], null=False)
    endereco = models.CharField(_('Endereço Completo'), max_length=255, null=False)
    aluno_uece = models.CharField(_('Você é aluno da FECLI-UECE?'), choices=aluno_uece_escolhas, max_length=10, null=False)
    como_conheceu = models.CharField(_('Como você conheceu o Eclass?'), choices=como_conheceu_escolhas, max_length=20, null=False)
    prioridades = models.CharField(_("Critérios de prioridades"), choices=priodades_escolhas, null=False)
    ocupacao = models.CharField(_('Qual a sua ocupação atual?'), max_length=255, null=False)
    motivacao = models.TextField(_('''Escreva aqui as suas motivações para participar no curso e também mencione as razões pelas quais você deve ser selecionada(o) para cursar o ECLASS. (Lembre de mencionar os critérios de prioridade listados anteriormente nos quais você se encaixa para a elaboração da resposta)'''), null=False)
    turma_entrada = models.CharField(_('Turma de entrada'), choices=turma_entrada_escolhas, max_length=10, null=False)
    termo_inscricao = models.CharField(_('''Declaro que li e concordo com os termos de inscrição referente ao período letivo 2024.1 do ECLASS, estando ciente de que o curso não efetuará a matrícula de alunos que fornecerem dados incorretos ou falsos'''), choices=termo_escolhas, max_length=5, null=False)

    def __str__(self):
        return self.nome_completo

class AnexosInscricao(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, related_name="anexos") 
    arquivo = models.FileField(_('Documentos'), upload_to="anexos/")

    def __str__(self):
        return f"Anexos do: {self.inscricao.nome_completo}"

class Provas(models.Model):
    id = models.AutoField(_('ID_Prova'), primary_key=True)
    conteudo = models.TextField(_('Conteúdo da prova'), null=False)
    data = models.DateField(_('Data'), null=False)
    tipo = models.CharField(_('Tipo da prova'), choices=tipo_prova_escolhas, max_length=30, null=False)
    objetivos = models.TextField(_('Objetivos'), null=False)

    def __str__(self):
        return f"{self.tipo} - {self.data}"

class AlunosProvas(models.Model):
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    prova = models.ForeignKey(Provas, verbose_name=_('Prova'), on_delete=models.CASCADE)
    nota = models.FloatField(_('Nota'), validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], null=False)

    def __str__(self):
        return f"Prova: {self.prova.tipo} Aluno: {self.aluno.nome_completo}"

class Aulas(models.Model):
    id = models.AutoField(_('ID_Aulas'), primary_key=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
    data = models.DateField(_('Data'), null=False)
    conteudo = models.TextField(_('Conteúdo da aula'), null=False)
    objetivos = models.TextField(_('Objetivos'), null=False)

    def __str__(self):
        return f"Aula da turma - {self.turma.semestre_letivo} dia - {self.data}"

class Frequencia(models.Model):
    id = models.AutoField(_('ID_Freq'), primary_key=True)
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    aula = models.ForeignKey(Aulas, verbose_name=_('Aula'), on_delete=models.CASCADE)
    presenca = models.BooleanField(_('Presença'), default=False)

class DadosBancarios(models.Model):
    id = models.AutoField(_('ID_DadosBanc'), primary_key=True)
    professor = models.ForeignKey(Professores, verbose_name=_('Professor'), on_delete=models.CASCADE)
    nome_banco = models.CharField(_('Nome do banco'), max_length=100, null=False)
    agencia = models.CharField(_('Nome da agência'), max_length=30, null=False)
    numero_conta = models.CharField(_('Número da conta'), max_length=50, null=False)
    tipo_conta = models.CharField(_('Tipo da conta'), max_length=50, null=False)

    def __str__(self):
        return f"Conta do professor - {self.professor.nome_completo}"

# FALTA REFAZER A TABELA INSCRIÇÃO E FAZER A TABELA ANEXOSINSCRICAO

anexos = models.FileField(_(""), upload_to=None, max_length=100)