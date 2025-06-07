from django.test import TestCase
from .models import Inscricao

class InscricaoTestCase(TestCase):
    def setUp(self):
        
        self.inscricao = Inscricao.objects.create(
            nome_completo="Maria",
            nome_social="Maria",
            dt_nasc="1999-12-31",
            cpf="321.654.987-00",
            email="maria@example.com",
            telefone="85998765432",
            endereco="Av. Central, 456",
            aluno_uece="Não",
            possui_deficiencia=True,
            qual_deficiencia="Visual",
            como_conheceu="Indicação",
            prioridades="Graduacao",
            ocupacao="Professora",
            motivacao="Melhorar o inglês para o trabalho",
            turma_entrada="turma_b",
            foto_frente="uploads/frente.jpg",
            foto_verso="uploads/verso.jpg",
            diploma_ensino_medio="uploads/diploma.jpg",
            termo_inscricao="Sim"
        )

    def test_nome_completo(self):
        self.assertEqual(self.inscricao.nome_completo, "Maria")
