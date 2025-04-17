# Projeto de Banco de Dados

## Integrantes do Grupo

* Pedro Henrique Ferreira Valim (R.A: 24.123.048-1)

* Rafael Takahagi Mendes (R.A: 24.123.050-7)

* Renan Casemiro Hessel (R.A: 24.123.019-2)

## Descrição
Este projeto representa a estrutura de um sistema acadêmico completo, implementado inteiramente em SQL, com foco em modelagem de dados para ambientes universitários. O objetivo é permitir o gerenciamento de departamentos, cursos, professores, disciplinas, alunos, históricos escolares e trabalhos de conclusão de curso (TCCs), utilizando relações bem definidas e integridade referencial.

## Funcionalidades

### 1. Departamentos
A tabela departamento representa os departamentos acadêmicos, como "Engenharia", "Ciência da Computação", etc. Cada departamento:

* Possui um nome único.

* Informa o número de matérias associadas.

* É chefiado por um professor, representado por uma chave estrangeira para a tabela professor.

### 2. Professores
A tabela professor armazena os docentes da instituição. Cada professor:

* Tem um identificador único.

* Está associado a um departamento.

* Pode atuar como chefe de um departamento ou coordenador de curso.

* Pode lecionar disciplinas específicas em determinados semestres (tabela ensina).

### 3. Cursos
A tabela curso representa os cursos oferecidos, como "Engenharia de Software" ou "Administração". Cada curso:

* Está vinculado a um departamento.

* É coordenado por um professor (chave estrangeira).

### 4. Disciplinas
A tabela disciplinas define as matérias que compõem os cursos. Cada disciplina:

* Possui um identificador e um nome.

* Está vinculada a um departamento.

* Informa a duração em semestres, carga horária teórica e prática.

### 5. Alunos
A tabela alunos armazena os estudantes da instituição. Cada aluno:

* Tem um ID e nome.

* Está associado a um departamento.

* Cursa apenas um curso no momento, não sendo possível cursar mais de 1 curso diferente no mesmo momento.

### 6. Histórico Escolar
A tabela hist_escolar registra as disciplinas cursadas pelos alunos. Ela funciona como um diário acadêmico, indicando:

* Qual disciplina foi cursada.

* Em que semestre e ano.

* Qual foi a nota final e o status (aprovado ou reprovado).

* A chave primária composta garante a unicidade de cada entrada para um aluno em uma disciplina, semestre e ano.

### 7. Ensina
A tabela ensina registra os professores que lecionam disciplinas, controlando:

* Qual professor ensinou qual disciplina.

* Em qual semestre e ano.

* Esse relacionamento permite múltiplos professores e múltiplas turmas ao longo do tempo.

### 8. TCCs
A tabela tccs armazena os trabalhos de conclusão de curso desenvolvidos por alunos, com:

* Um ID

* Um título.

* Um orientador (nome livre, não chave estrangeira).

### 9. Alunos e TCCs
A tabela tccs_alunos representa a associação entre TCCs e seus autores. Permite:

* Trabalhos com um ou mais alunos.

* Registro de trabalhos em grupo caso mais de um aluno tenha o TCC com mesmo ID.

## Execução 

Primeiro, utilize o arquivo ddl.sql para criar as tabelas no banco de dados. Em seguida, execute o script dados.py para gerar dados para o banco com os dados, preenchendo previamente o arquivo info.env com suas variáveis de acesso. Após essa etapa, você pode utilizar livremente as demais queries disponíveis.

## Queries SQL

1. Histórico escolar com reprovações e aprovações subsequentes
Apresenta todas as tentativas do aluno em uma determinada disciplina, incluindo eventuais reprovações e a aprovação obtida posteriormente.

2. Trabalhos de Conclusão de Curso (TCC) orientados por um professor
Lista todos os projetos de TCC supervisionados por um professor, juntamente com os nomes dos alunos responsáveis por cada trabalho.

3. Comparação de matrizes curriculares entre dois cursos com disciplinas em comum
Foram realizadas duas consultas, uma para cada curso (por exemplo, Ciência da Computação e Ciência de Dados), listando todas as disciplinas de cada um e permitindo identificar aquelas que são compartilhadas entre ambos.

4. Disciplinas cursadas por um aluno com os respectivos professores
Apresenta os nomes e códigos das disciplinas que um aluno cursou, acompanhados dos nomes dos professores responsáveis por cada uma delas.

5. Chefes de departamento e coordenadores de curso
Exibe os nomes dos professores, juntamente com o nome do departamento que chefiam e o curso que coordenam. 
  
## Modelos

![image](https://github.com/user-attachments/assets/e4e13590-af44-4960-9765-cc7396589aeb)

![image](https://github.com/user-attachments/assets/ff34a8a2-5fdf-4815-9bbf-8ffb56d278ae)



