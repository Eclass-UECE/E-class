# Sistema de Gerenciamento do Curso ECLASS

Este sistema foi desenvolvido como projeto no curso de Ciência da Computação, durante o quinto período no IFCE - campus Iguatu. Seu principal objetivo é atender às necessidades do projeto de extensão ECLASS, oferecido pela UECE - Iguatu, por meio da criação de um "professor online" voltado para a inscrição e o gerenciamento de alunos no curso.

---

## 📘 ECLASS - English Class

ECLASS é um curso básico de inglês ofertado gratuitamente pela Universidade Estadual do Ceará (UECE) - FECLI Campus Iguatu. O curso tem como objetivo promover o ensino de inglês para a comunidade, contemplando alunos iniciantes, com conhecimento prévio e egressos.

---

## ⚙️ Funcionalidades

### 1. Inscrição de Novos Alunos

Os interessados no curso podem se inscrever por meio de três formulários distintos:

- **Iniciante (S1):** para alunos sem conhecimento prévio.  
- **Teste de Nivelamento:** para alunos com algum conhecimento em inglês.  
- **Egressos:** para antigos alunos que desejam retornar ou avançar no curso.

Os dados das inscrições são armazenados e disponibilizados aos coordenadores, que poderão gerar listas de aprovados por turma e modalidade.

### 2. Login de Professores e Coordenadores

- Professores e coordenadores podem acessar o sistema por meio de login baseado em sessões PHP.
- As credenciais e demais informações são armazenadas em um banco de dados PostgreSQL.
- Após o login, os usuários são redirecionados para áreas específicas conforme seu perfil.

### 3. Página do Professor e do Coordenador

- **Professores:** possuem uma área para lançar notas, registrar faltas e descrever os conteúdos ministrados nas aulas.
- **Coordenadores:** têm acesso a essas informações através da funcionalidade de "entrega de diário", podendo acompanhar o desempenho das turmas e dos professores.

---

## 💻 Tecnologias Utilizadas

- **Frontend:** HTML, CSS  
- **Backend:** Python, Django  
- **Banco de Dados:** PostgreSQL  
- **Ferramentas de Desenvolvimento:** VS Code, Miro, Taiga, Figma  
