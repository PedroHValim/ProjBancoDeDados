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


        # Listas de valores realistas
    departamentos = ['Ciência da Computação', 'Engenharia',  'Matemática', 'Biologia', 'História']
    disciplinas_por_departamento = {
        "Ciência da Computação": [
            "Programação", "Estruturas de Dados", "Banco de Dados", "Redes de Computadores", 
            "Inteligência Artificial", "Segurança da Informação", "Computação Gráfica"
        ],
        "Engenharia": [
            "Cálculo Diferencial e Integral", "Mecânica dos Sólidos", "Termodinâmica", 
            "Eletromagnetismo", "Desenho Técnico", "Materiais de Engenharia"
        ],
        "Matemática": [
            "Álgebra Linear", "Cálculo Numérico", "Probabilidade e Estatística", 
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
    alunos = []                                                                 
    professores = []
    cursos_ = []
    hist_id_ = []
    tcc_id = []

    # Gerando departamentos
    for _ in range(5):
        depto = departamentos[_]
        num_materias = random.randint(5, 20)
        cursor.execute(f"insert into departamento values ('{depto}', {num_materias});")

    # Gerando professores
    for _ in range(10):
        id_prof = fake.unique.random_int(min=1000, max=9999)
        professores.append(id_prof)
        nome = fake.name()
        depto = random.choice(departamentos)
        cursor.execute(f"insert into professor values ('{id_prof}', '{nome}', '{depto}');")

    #Gerando o chefe de cada departamento
    chefes = random.sample(professores,5)
    for _ in range(5):
        chefe = chefes[_]
        nome_dpto = departamentos[_]
        cursor.execute(f"update departamento set chefe = '{chefe}' where nome_dpt = '{nome_dpto}' ;")


    # Gerando cursos
    coord = random.sample(professores,5)
    for _ in range(5):
        codigo = fake.unique.bothify(text='???-###')
        cursos_.append(codigo)
        depto = random.choice(departamentos)
        nome = random.choice(cursos_por_departamento[depto])
        coord2 = coord[_]
        cursor.execute(f"insert into curso values ('{codigo}', '{nome}', '{depto}','{coord2}');")

    # Gerando alunos
    for _ in range(10):
        id_aluno = fake.unique.random_int(min=1000, max=9999)
        alunos.append(id_aluno)
        nome = fake.name()
        depto = random.choice(departamentos)
        cursor.execute(f"insert into alunos values ('{id_aluno}', '{nome}', '{depto}');")

    # Gerando disciplinas
    for _ in range(5):
        codigo = fake.unique.bothify(text='D###')
        depto = random.choice(departamentos)
        dsic = random.choice(disciplinas_por_departamento[depto])
        semestres = random.randint(2, 4)
        aula_teo = semestres * 15
        aula_pra = semestres * 10
        cursor.execute(f"insert into disciplinas values ('{codigo}', '{dsic}', '{depto}', {semestres}, {aula_teo}, {aula_pra});")

    # Gerando histórico escolar
    for _ in range(15):
        curso_id = random.choice(cursos_)
        hist_id = fake.unique.bothify(text='???-####')
        semestre = random.randint(1, 4)
        ano = random.randint(2015, 2024)
        aluno_id = random.choice(alunos)
        nota = round(random.uniform(0, 10), 1)
        if(nota >= 5):
            status = "Aprovado" 
        else:
            status = "Reprovado"
        hist_id_.append((curso_id, hist_id, semestre, ano)) 
        cursor.execute(f"insert into hist_escolar values ('{curso_id}', '{hist_id}', '{aluno_id}', {semestre}, {ano}, '{status}', {nota});")

    # Gerando ensina
    for _ in range(5):
        professor_id = random.choice(professores)
        curso_id, hist_id, semestre, ano = random.choice(hist_id_)  
        cursor.execute(f"insert into ensina values ('{professor_id}', '{curso_id}', '{hist_id}', {semestre}, {ano});")


    # Gerando TCCs
    for _ in range(5):
        codigo_tcc = fake.unique.bothify(text='TCC##')
        tcc_id.append(codigo_tcc)
        titulo = fake.sentence(nb_words=3)
        professor_id = random.choice(professores)
        cursor.execute(f"insert into tccs values ('{codigo_tcc}', '{titulo}', '{professor_id}');")

    # Gerando TCCs-Alunos
    for _ in range(5):
        codigo_tcc = random.choice(tcc_id)
        aluno_id = random.choice(alunos)
        cursor.execute(f"insert into tccs_alunos values ('{codigo_tcc}', '{aluno_id}');")

    cursor.execute("commit")

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")



except Exception as e:
    print(f"Failed to connect: {e}")