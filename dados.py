from faker import Faker
import random

fake = Faker()

#senha bando de dados:  bancodedados123

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv('info.env')

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    cursor.execute("delete from tccs_alunos;")
    cursor.execute("delete from departamento;")
    cursor.execute("delete from alunos;")
    cursor.execute("delete from professor;")
    cursor.execute("delete from disciplinas;")
    cursor.execute("delete from curso;")
    cursor.execute("delete from ensina;")
    cursor.execute("delete from hist_escolar;")
    cursor.execute("delete from tccs;")
    cursor.execute("ALTER SEQUENCE hist_escolar_id_hist_seq RESTART WITH 1")


    # Listas de valores realistas
    departamentos = ['Ciência da Computação', 'Engenharia',  'Matemática', 'Biologia', 'História']
    disciplinas_por_departamento = {
        "Ciência da Computação": [
            "Programação", "Estruturas de Dados", "Banco de Dados", "Cálculo", 
            "Inteligência Artificial", "Segurança da Informação"
        ],
        "Engenharia": [
            "Cálculo", "Mecânica dos Sólidos", "Termodinâmica", 
            "Eletromagnetismo", "Desenho Técnico", "Materiais de Engenharia"
        ],
        "Matemática": [
            "Álgebra Linear", "Cálculo", "Probabilidade e Estatística", 
            "Teoria dos Números", "Geometria Analítica", "Modelagem Matemática"
        ],
        "Biologia": [
            "Genética", "Ecologia", "Fisiologia Humana", 
            "Microbiologia", "Biologia Celular", "Zoologia"
        ],
        "História": [
            "História Antiga", "História Medieval", "História do Brasil", 
            "História Contemporânea", "História da Arte", "História Econômica"
        ]
    }

    cursos = ['Ciência da Computação', 'Engenharia de Produção', 'Engenharia de Automação','Engenharia Quiímica', 'Matemática', 'História', 'Biologia']

    cursos_por_departamento = {
        "Ciência da Computação": ["Ciência da Computação"],
        "Engenharia": ["Engenharia de Produção", "Engenharia de Automação", "Engenharia Química"],
        "Matemática": ["Matemática"],
        "Biologia": ["Biologia"],
        "História": ["História"]
    }
    professores_por_departamento = {
        "Ciência da Computação": [],
        "Engenharia": [],
        "Matemática": [],
        "Biologia": [],
        "História": []
    }
    alunos = []                                                                 
    professores = []
    cursos_ = []
    tcc_id = []

    # Gerando departamentos
    for _ in range(5):
        depto = departamentos[_]
        num_materias = random.randint(5, 20)
        cursor.execute(f"insert into departamento values ('{depto}', {num_materias});")

    # Gerando professores
    for i in range(5):
        depto = departamentos[i]
        for _ in range(3):
            id_prof = fake.unique.random_int(min=1000, max=9999)
            professores.append(id_prof)
            nome = fake.name()
            professores_por_departamento[depto].append(id_prof)
            cursor.execute(f"insert into professor values ('{id_prof}', '{nome}', '{depto}');")

    #Gerando o chefe de cada departamento
    for _ in range(5):
        nome_dpto = departamentos[_]
        chefe = random.choice(professores_por_departamento[nome_dpto])
        cursor.execute(f"update departamento set chefe = '{chefe}' where nome_dpt = '{nome_dpto}' ;")

    # Gerando cursos
    for depto, cursos in cursos_por_departamento.items():
        professores = professores_por_departamento[depto]
        for nome, coord2 in zip(cursos, professores): #desta forma é possível termos um professor especifico do dpto para cada curso
            codigo = fake.unique.bothify(text='???-###')
            cursos_.append(codigo)
            cursor.execute(f"insert into curso values ('{codigo}', '{nome}', '{depto}', '{coord2}');")



    # Gerando alunos
    for _ in range(30):
        id_aluno = fake.unique.random_int(min=1000, max=9999)
        alunos.append(id_aluno)
        nome = fake.name()
        depto = random.choice(departamentos)
        cursor.execute(f"insert into alunos values ('{id_aluno}', '{nome}', '{depto}');")

    # Gerando disciplinas
    for _ in range(5):
        depto = departamentos[_]
        for i in range(6):
            codigo = fake.unique.bothify(text='D###')
            dsic = disciplinas_por_departamento[depto][i]
            semestres = random.randint(2, 4)
            aula_teo = semestres * 15
            aula_pra = semestres * 10
            cursor.execute(f"insert into disciplinas values ('{codigo}', '{dsic}', '{depto}', {semestres}, {aula_teo}, {aula_pra});")

    # Gerando histórico escolar
    for _ in range(15):
        curso_id = random.choice(cursos_)
        semestre = random.randint(1, 2)
        ano = random.randint(2015, 2024)
        aluno_id = random.choice(alunos)
        nota = round(random.uniform(0, 10), 1)
        if(nota >= 5):
            status = "Aprovado" 
        else:
            status = "Reprovado" 
        cursor.execute(f"""insert into hist_escolar (id_curso, semestre, ano, aluno, status, nota) 
                       values ('{curso_id}',  '{semestre}', {ano}, {aluno_id}, '{status}', {nota});""")
        if status == "Reprovado":
            if semestre == 1:
                cursor.execute(f"""insert into hist_escolar (id_curso, semestre, ano, aluno, status, nota) 
                       values ('{curso_id}',  '{semestre + 1}', {ano}, {aluno_id}, '{"Aprovado"}', {random.randint(5,10)});""")
            elif semestre == 2:
                cursor.execute(f"""insert into hist_escolar (id_curso, semestre, ano, aluno, status, nota) 
                       values ('{curso_id}',  '{semestre - 1}', {ano + 1}, {aluno_id}, '{"Aprovado"}', {random.randint(5,10)});""")

    cursor.execute("commit")
    cursor.close()
    cursor = connection.cursor()

    # Gerando ensina
    for _ in range(10):
        professor_id = random.choice(professores)
        cursor.execute(f"select nome_dpt from professor where id = '{professor_id}'")
        nome_dpt2 = cursor.fetchone()[0]
        cursor.execute(f"select id from disciplinas where departamento = '{nome_dpt2}'")
        id_disc = cursor.fetchone()[0]
        semestre = random.randint(1, 2)
        ano = random.randint(2000, 2024)
        cursor.execute(f"insert into ensina values ('{professor_id}', '{id_disc}', {semestre}, {ano});")


    # Gerando TCCs
    for _ in range(5):
        codigo_tcc = fake.unique.bothify(text='TCC##')
        tcc_id.append(codigo_tcc)
        titulo = fake.sentence(nb_words=3)
        professor_id = random.choice(professores)
        cursor.execute(f"insert into tccs values ('{codigo_tcc}', '{titulo}', '{professor_id}');")

    # Gerando TCCs-Alunos
    for _ in tcc_id:
        aluno_id = random.sample(alunos,4)
        for aluno in aluno_id:
            cursor.execute(f"insert into tccs_alunos values ('{_}', '{aluno}');")

    cursor.execute("commit")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")



except Exception as e:
    print(f"Failed to connect: {e}")