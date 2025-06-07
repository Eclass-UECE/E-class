from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .validators import validar_cpf, validar_rg, validar_telefone
from django.core.exceptions import ValidationError


# -----------------------------
# Constantes (choices)
# -----------------------------

turnos_escolhas = [('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')]

aluno_uece_escolhas = [('Sim', 'Sim'), ('Não', 'Não'), ('Outro', 'Outro')]

termo_escolhas = [('Sim', 'Sim'), ('Não', 'Não')]

como_conheceu_escolhas = [
    ('Rede_Social', 'Rede Social'), ('Indicação', 'Indicação'),
    ('TV', 'TV'), ('Outro', 'Outro')
]

turma_entrada_escolhas = [
    ('turma_a', 'S01 - Turma A: sábado, manhã 08h às 11h40'),
    ('turma_b', 'S01 - Turma B: sábado, tarde 13h às 16h40.'),
    ('testenivel', 'Desejo realizar o teste de nivel para entrar em uma turma mais avançada.')
]

tipo_prova_escolhas = [
    ('Writing', 'Writing'),
    ('Use_of_english', 'Use of english'),
    ('Speaking', 'Speaking'),
    ('Listening', 'Listening')
]

priodades_escolhas = [
    ('Nenhum', 'Não me enquadro em nenhuma das categorias'),
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
    ('Servidor_publi', 'Servidor público')
]

deficiencia_choices = [
    ('Física', 'Física'), ('Auditiva', 'Auditiva'),
    ('Visual', 'Visual'), ('Intelectual', 'Intelectual'),
    ('Múltipla', 'Múltipla'), ('Outra', 'Outra')
]

situacao_choices = [('Cursando', 'Cursando'), ('Aprovado', 'Aprovado'), ('Reprovado', 'Reprovado')]

# -----------------------------
# Funções auxiliares
# -----------------------------

def upload_path(instance, filename):
    if hasattr(instance, 'inscricao'):
        return f"uploads/Inscricao_{instance.inscricao.nome_completo}/{filename}"
    elif hasattr(instance, 'cpf'):
        return f"uploads/Inscricao_{instance.nome_completo}/{filename}"

# -----------------------------
# Modelos principais
# -----------------------------

class Inscricao(models.Model):
    # Dados pessoais e inscrição
    id_inscricao = models.AutoField(_('ID'), primary_key=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255)
    nome_social = models.CharField(_('Nome Social'), max_length=255, null=True)
    dt_nasc = models.DateField(_('Data de nascimento'))
    cpf = models.CharField(_('CPF'), max_length=14)
    email = models.EmailField(_('Email'))
    telefone = models.CharField(_('Telefone (WhatsApp)'), max_length=12)
    endereco = models.CharField(_('Endereço Completo'), max_length=255)
    aluno_uece = models.CharField(_('Você é aluno da FECLI-UECE'), choices=aluno_uece_escolhas)
    possui_deficiencia = models.BooleanField(_('Possui deficiência'), default=False)
    qual_deficiencia = models.CharField(_('Tipo de deficiência'), choices=deficiencia_choices, null=True, blank=True)
    como_conheceu = models.CharField(_('Como conheceu o Eclass'), choices=como_conheceu_escolhas, max_length=20)
    prioridades = models.CharField(_("Critérios de prioridades"), choices=priodades_escolhas)
    ocupacao = models.CharField(_('Ocupação atual'), max_length=255)
    motivacao = models.TextField(_('Motivação para o curso'), null=False)
    turma_entrada = models.CharField(_('Turma de entrada'), choices=turma_entrada_escolhas, max_length=50)
    foto_frente = models.FileField(_('Foto identidade - frente'), upload_to=upload_path)
    foto_verso = models.FileField(_('Foto identidade - verso'), upload_to=upload_path)
    diploma_ensino_medio = models.FileField(_('Diploma Ensino Médio'), upload_to=upload_path)
    termo_inscricao = models.CharField(_('Termo de inscrição'), choices=termo_escolhas, max_length=5)
    teste_nivel = models.CharField(_('Turma teste de nivel'), max_length=100, null=True, blank=True)
    aprovado = models.BooleanField(_("Aprovado"), default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Inscrições"

    def __str__(self):
        return self.nome_completo

class Coordenadores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True)
    rg = models.CharField(_('RG'), max_length=12, unique=True)
    telefone = models.CharField(_('Telefone'), max_length=12)
    email = models.EmailField(_('Email'))

    class Meta:
        verbose_name_plural = "Coordenadores"

    def __str__(self):
        return self.nome_completo

class Professores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True)
    rg = models.CharField(_('RG'), max_length=9, unique=True)
    telefone = models.CharField(_('Telefone'), max_length=12)
    dt_nasc = models.DateField(_('Data de nascimento'))
    email = models.EmailField(_('Email'))
    endereco = models.CharField(_('Endereço'), max_length=255)
    semestre_ingressao = models.CharField(_('Semestre de Ingresso'), max_length=6)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20)
    primeiro_acesso = models.BooleanField(_('Primeiro Acesso'), default=False, null=True, blank=True)
    diarios = models.ManyToManyField('Diario', verbose_name=_('Diários'), blank=True)

    class Meta:
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo

class Turmas(models.Model):
    id_turma = models.AutoField(_('ID_Turma'), primary_key=True)
    semestre_letivo = models.CharField(_('Semestre da turma'), max_length=6)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20)
    sala = models.CharField(_('Sala'), max_length=10)
    num_vagas = models.PositiveIntegerField(_('Vagas'))
    professor = models.ForeignKey(Professores, verbose_name=_('Professor'), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"Turma {self.id_turma} - {self.semestre_letivo}"

class Alunos(models.Model):
    matricula = models.AutoField(_('Matricula'), primary_key=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255)
    cpf = models.CharField(_('CPF'), max_length=14)
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone])
    dt_nasc = models.DateField(_('Data de nascimento'))
    email = models.EmailField(_('Email'))
    instituicao_ensino = models.CharField(_('Instituição de ensino'), max_length=255)
    ocupacao = models.CharField(_('Ocupação'), max_length=255)
    semestre = models.PositiveIntegerField(_('Semestre'), validators=[MinValueValidator(1), MaxValueValidator(6)])
    relatorio = models.TextField(_('Relatório'), null=True, blank=True)
    situacao = models.CharField(_("Situação"), choices=situacao_choices, max_length=255)
    confirmacao_egresso = models.BooleanField(_("Pedido de rematrícula"), default=False, null=True, blank=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
    inscricao = models.ForeignKey(Inscricao, verbose_name=_('Inscrição'), on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.nome_completo

# -----------------------------
# Modelos auxiliares e relacionais
# -----------------------------

class AnexosInscricao(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to=upload_path)
    data_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Anexos das Inscrições"

    def __str__(self):
        return f"Anexo de {self.inscricao} enviado em {self.data_upload.strftime('%d/%m/%Y %H:%M')}"

class Provas(models.Model):
    id_prova = models.AutoField(_('ID_Prova'), primary_key=True)
    conteudo = models.TextField(_('Conteúdo da prova'))
    data = models.DateField(_('Data'))
    tipo = models.CharField(_('Tipo da prova'), choices=tipo_prova_escolhas, max_length=30)
    objetivos = models.TextField(_('Objetivos'))

    class Meta:
        verbose_name_plural = "Provas"

    def __str__(self):
        return f"{self.tipo} - {self.data}"

class AlunosProvas(models.Model):
    id_alunosprova = models.AutoField(_("ID_Alunosprova"), primary_key=True)
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    prova = models.ForeignKey(Provas, verbose_name=_('Prova'), on_delete=models.CASCADE)
    nota = models.FloatField(_('Nota'), validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    class Meta:
        verbose_name_plural = "Notas"

    def __str__(self):
        return f"Prova: {self.prova.tipo} Aluno: {self.aluno.nome_completo}"

class Aulas(models.Model):
    id_aulas = models.AutoField(_('ID_Aulas'), primary_key=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
    data = models.DateField(_('Data'))
    conteudo = models.TextField(_('Conteúdo da aula'))
    objetivos = models.TextField(_('Objetivos'))

    class Meta:
        verbose_name_plural = "Aulas"

    def __str__(self):
        return f"Aula da turma - {self.turma.semestre_letivo} dia - {self.data}"

class Frequencia(models.Model):
    id_frequencia = models.AutoField(_('ID_Freq'), primary_key=True)
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    aula = models.ForeignKey(Aulas, verbose_name=_('Aula'), on_delete=models.CASCADE)
    presenca = models.BooleanField(_('Presença'), default=False)

    class Meta:
        verbose_name_plural = "Frequência dos alunos"

    def __str__(self):
        return f"Frequência do aluno:{self.aluno.nome_completo} dia - {self.aula.data}"

class Diario(models.Model):
    id_diario = models.AutoField(_('ID_Diario'), primary_key=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
    data = models.DateField(_('Data'), auto_now_add=True)
    conteudo = models.TextField(_('Conteúdo da aula'))
    objetivos = models.TextField(_('Objetivos da aula'))
    observacoes = models.TextField(_('Observações'), blank=True, null=True)

    class Meta:
        verbose_name_plural = "Diários"
        ordering = ['-data']

    def __str__(self):
        return f"Diário {self.turma} - {self.data}"

class RegistroDiario(models.Model):
    diario = models.ForeignKey(Diario, verbose_name=_('Diário'), on_delete=models.CASCADE)
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    presente = models.BooleanField(_('Presente'), default=True)
    participacao = models.PositiveIntegerField(_('Participação'), validators=[MinValueValidator(0), MaxValueValidator(5)], default=3)
    tarefa = models.PositiveIntegerField(_('Tarefa'), validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    observacoes = models.TextField(_('Observações do aluno'), blank=True, null=True)
    prova = models.ForeignKey(AlunosProvas, on_delete=models.CASCADE, null=True, blank=True)


    
    def clean(self):
        if self.aluno.turma != self.diario.turma:
            raise ValidationError("O aluno não pertence a esta turma.")
        
    class Meta:
        verbose_name_plural = "Registros Diários"
        unique_together = [['diario', 'aluno']]

    def __str__(self):
        return f"{self.aluno} - {self.diario}"

class AlunosTurmas(models.Model):
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
