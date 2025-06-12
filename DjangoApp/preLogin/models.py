from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .validators import validar_cpf, validar_rg, validar_telefone

def upload_path(instance, filename):
    # Para AnexosInscricao, use instance.inscricao.cpf
    if hasattr(instance, 'inscricao'):
        return f"uploads/Inscricao_{instance.inscricao.nome_completo}/{filename}"
    # Para Inscricao diretamente (se necessário)
    elif hasattr(instance, 'cpf'):
        return f"uploads/Inscricao_{instance.nome_completo}/{filename}"

turnos_escolhas = [
    ('Matutino', 'Matutino'),
    ('Vespertino', 'Vespertino'),
]

aluno_uece_escolhas = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Outro', 'Outro')
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

turma_entrada_escolhas = [
    ('turma_a','S01 - Turma A: sábado, manhã 08h às 11h40'),
    ('turma_b','S01 - Turma B: sábado, tarde 13h às 16h40.'),
    ('testenivel','Desejo realizar o teste de nivel para entrar em uma turma mais avançada.')
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
    ('Física', 'Física'),
    ('Auditiva', 'Auditiva'),
    ('Visual', 'Visual'),
    ('Intelectual', 'Intelectual'),
    ('Múltipla', 'Múltipla'),
    ('Outra', 'Outra')
]

situacao_choices = [('Cursando', 'Cursando'),
                    ('Aprovado', 'Aprovado'),
                    ('Reprovado', 'Reprovado')]


class Professores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True, validators=[validar_cpf], null=False)
    rg = models.CharField(_('RG'), max_length=11, unique=True, validators=[validar_rg], null=False)
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    email = models.EmailField(_('Email'), null=False)
    endereco = models.CharField(_('Endereço'), max_length=255, null=False)
    semestre_ingressao = models.CharField(_('Semestre de Ingresso'), max_length=6,null=False)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20, null=False)
    primeiro_acesso = models.BooleanField(_('Primeiro Acesso'), default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo

class Turmas(models.Model):
    id_turma = models.AutoField(_('ID_Turma'), primary_key=True)
    semestre_letivo = models.CharField(_('Semestre da turma'), max_length=1, null=False)
    semestre_atual = models.CharField(_('Semestre atual'), max_length=6, null=False)
    turno = models.CharField(_('Turno'), choices=turnos_escolhas, max_length=20, null=False)
    sala = models.CharField(_('Sala'), max_length=10, null=False)
    num_vagas = models.PositiveIntegerField(_('Vagas'), null=False)
    professor = models.ForeignKey(Professores, verbose_name=_('Professor'), on_delete=models.CASCADE, null=True, blank=True)
    numero_turma = models.CharField(_('Numero da turma'), max_length=1, null=False)

    class Meta:
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"Turma {self.id_turma} - {self.semestre_letivo}"

class Inscricao(models.Model):
    id_inscricao = models.AutoField(_('ID'), primary_key=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    nome_social = models.CharField(_('Nome Social'), max_length=255, null=True)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    cpf = models.CharField(_('CPF'), max_length=14, validators=[validar_cpf])
    email = models.EmailField(_('Email'), null=False)
    telefone = models.CharField(_('Telefone (WhatsApp)'), max_length=12, null=False)
    endereco = models.CharField(_('Endereço Completo'), max_length=255, null=False)
    aluno_uece = models.CharField(_('Você é aluno da FECLI-UECE'), choices=aluno_uece_escolhas, null=False)
    possui_deficiencia = models.BooleanField(_('Possui deficiência'), null=False, default=False)
    qual_deficiencia = models.CharField(_('Se sim selecione o tipo de deficiência'), choices=deficiencia_choices, null=True, blank=True)
    como_conheceu = models.CharField(_('Como você conheceu o Eclass'), choices=como_conheceu_escolhas, max_length=20, null=False)
    prioridades = models.CharField(_("Critérios de prioridades"), choices=priodades_escolhas, null=False)
    ocupacao = models.CharField(_('Qual a sua ocupação atual?'), max_length=255, null=False)
    motivacao = models.TextField(_('''Escreva aqui as suas motivações para participar no curso e também mencione as razões pelas quais você deve ser selecionada(o) para cursar o ECLASS. (Lembre de mencionar os critérios de prioridade listados anteriormente nos quais você se encaixa para a elaboração da resposta)'''), null=False)
    turma_entrada = models.CharField(_('Turma de entrada'), choices=turma_entrada_escolhas, max_length=50, null=False)
    foto_frente = models.FileField(_('Foto da identidade (Frente)'), upload_to=upload_path, null=False)
    foto_verso = models.FileField(_('Foto da identidade (Verso)'), upload_to=upload_path, null=False)
    diploma_ensino_medio = models.FileField(_('Foto do diploma do ensino médio'), upload_to=upload_path, null=False)
    termo_inscricao = models.CharField(_('''Declaro que li e concordo com os termos de inscrição referente ao período letivo 2024.1 do ECLASS, estando ciente de que o curso não efetuará a matrícula de alunos que fornecerem dados incorretos ou falsos'''), choices=termo_escolhas, max_length=5, null=False)
    teste_nivel = models.CharField(_('Turma teste de nivel'), max_length=100, null=True, blank=True)
    aprovado = models.BooleanField(_("Aprovado"),default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Inscrições"

    def __str__(self):
        return self.nome_completo

class Alunos(models.Model):
    matricula = models.AutoField(_('Matricula'), primary_key=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=14, validators=[validar_cpf])
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    dt_nasc = models.DateField(_('Data de nascimento'), null=False)
    email = models.EmailField(_('Email'), null=False)
    instituicao_ensino = models.CharField(_('Instituição de ensino'), max_length=255, null=False)
    ocupacao = models.CharField(_('Ocupação'), max_length=255, null=False)
    semestre = models.PositiveIntegerField(_('Semestre'), validators=[MinValueValidator(1), MaxValueValidator(6)], null=False)
    relatorio = models.TextField(_('Relatório'), null=True, blank=True)
    situacao = models.CharField(_("Situacão"), max_length=255, choices=situacao_choices, null=False)
    confirmacao_egresso = models.BooleanField(_("Pedido de rematricula"), default=False, null=True, blank=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)
    inscricao = models.ForeignKey(Inscricao, verbose_name=_('Inscrição'), on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.nome_completo
    

class AlunosTurmas(models.Model):
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE)


class Coordenadores(models.Model):
    matricula = models.PositiveIntegerField(primary_key=True)
    senha = models.CharField(_('Senha'), default="12345678", max_length=30, blank=True)
    nome_completo = models.CharField(_('Nome completo'), max_length=255, null=False)
    cpf = models.CharField(_('CPF'), max_length=14, unique=True, validators=[validar_cpf], null=False)
    rg = models.CharField(_('RG'), max_length=11, unique=True, validators=[validar_rg], null=False)
    telefone = models.CharField(_('Telefone'), max_length=12, validators=[validar_telefone], null=False)
    email = models.EmailField(_('Email'), null=False)

    class Meta:
        verbose_name_plural = "Coordenadores"

    def __str__(self):
        return self.nome_completo

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
    conteudo = models.TextField(_('Conteúdo da prova'), null=False)
    data = models.DateField(_('Data'), null=False)
    tipo = models.CharField(_('Tipo da prova'), choices=tipo_prova_escolhas, max_length=30, null=False)
    objetivos = models.TextField(_('Objetivos'), null=False)

    class Meta:
        verbose_name_plural = "Provas"

    def __str__(self):
        return f"{self.tipo} - {self.data}"

class AlunosProvas(models.Model):
    id_alunosprova = models.AutoField(_("ID_Alunosprova"), primary_key=True)
    aluno = models.ForeignKey(Alunos, verbose_name=_('Aluno'), on_delete=models.CASCADE)
    prova = models.ForeignKey(Provas, verbose_name=_('Prova'), on_delete=models.CASCADE)
    nota = models.FloatField(_('Nota'), validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], null=False)

    class Meta:
        verbose_name_plural = "Notas"

    def __str__(self):
        return f"Prova: {self.prova.tipo} Aluno: {self.aluno.nome_completo}"

class Aulas(models.Model):
    id_aulas = models.AutoField(_('ID_Aulas'), primary_key=True)
    turma = models.ForeignKey(Turmas, verbose_name=_('Turma'), on_delete=models.CASCADE, null=False)
    data = models.DateField(_('Data'), null=False)
    conteudo = models.TextField(_('Conteúdo da aula'), null=False)
    objetivos = models.TextField(_('Objetivos'), null=False)
    
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

class DadosBancarios(models.Model):
    id_dadosbanc = models.AutoField(_('ID_DadosBanc'), primary_key=True)
    professor = models.ForeignKey(Professores, verbose_name=_('Professor'), on_delete=models.CASCADE)
    nome_banco = models.CharField(_('Nome do banco'), max_length=100, null=False)
    agencia = models.CharField(_('Número da agência'), max_length=30, null=False)
    numero_conta = models.CharField(_('Número da conta'), max_length=50, null=False)

    class Meta:
        verbose_name_plural = "Dados Bancários"

    def __str__(self):
        return f"Conta do professor - {self.professor.nome_completo}"