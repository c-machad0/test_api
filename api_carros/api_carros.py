from flask import Flask, make_response, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() # Carrega as variaveis do .env

mydb = mysql.connector.connect( # Conectando ao banco de dados usando variaveis de ambiente
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),  
    database=os.getenv("DB_NAME")
)

app = Flask(__name__) # Instanciando variável e usando o nome do modulo como nome da API
app.config['JSON_SORT_KEYS'] = False # Para que o flask não ordene alfabeticamente as requisições enviadas

@app.route('/carros', methods=['GET'])
def get_carros(): # Criei uma função que retorna os carros e marquei a função para mostrar que é uma rota da API
    
    my_cursor = mydb.cursor() # inicializa o cursor
    my_cursor.execute('SELECT * FROM carros') # carrega dentro do cursor, todos os carros do banco de dados
    meus_carros = my_cursor.fetchall() # fetchall retorna a lista de todos os dados que conseguiu capturar no SQL
    
    carros = list() # Instancio uma lista de nova vazia
    for carro in meus_carros: # Para cada carro da minha tabela, adiciono na lista de carros e haverá um retorno estruturado
        carros.append(
            {
                'id': carro[0],
                'marca': carro[1],
                'modelo': carro[2],
                'ano': carro[3]
            }
        )

    return make_response( # make_responsa ajuda a construir uma resposta de APIs
        jsonify(
            mensagem='Lista de carros.',
            dados=carros
        ) # jsonify retorna a resposta em formato json (formato padrão de respostas de APIs)
    )

@app.route('/carros', methods=['POST'])
def create_carro():
    carro = request.json # Capturando o carro da requisição em armazenando na variável carro
    
    my_cursor = mydb.cursor()

    sql = "INSERT INTO carros (marca, modelo, ano) VALUES (%s, %s, %s)"
    valores = (carro["marca"], carro["modelo"], carro["ano"])

    my_cursor.execute(sql, valores) # Executando o comando SQL de inserção de dados

    mydb.commit() # Ao executar o comando, precisa-se registar a transação com o commmit

    return make_response(
        jsonify(
            mensagem='Carro cadastrado com sucesso.',
            carro=carro
        )
    )

app.run() # Rodando a API