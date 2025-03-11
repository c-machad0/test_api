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
    modelo = carro.get('modelo') # Recebe o modelo do carro

    sql_check = "SELECT * FROM carros WHERE modelo = %s" # Busca todos os carros com o modelo especificado no banco de dados
    valores_check = (modelo,) # Armazena o modelo dentro de uma tupla. O uso da vírgula é para garantir que seja tratado como uma tupla de um único elemento
    my_cursor.execute(sql_check, valores_check) # Executa a consulta SQL com o modelo como parâmetro, de forma segura
    resultado = my_cursor.fetchall() # Armazena o resultado das consultas em uma lista de tuplas

    if not resultado: # Se não exister dentro da lista 
        insert_sql = "INSERT INTO carros (marca, modelo, ano) VALUES (%s, %s, %s)" # Insere na tabela carros valores de marca, modelo e ano
        values_insert = (carro["marca"], carro["modelo"], carro["ano"]) # Armazena os valores de marca, modelo e ano

        my_cursor.execute(insert_sql, values_insert) # Executando o comando SQL de inserção de dados

        mydb.commit() # Ao executar o comando, precisa-se registar a transação com o commmit

        return make_response(
            jsonify(
                mensagem='Carro cadastrado com sucesso.', # Retorna o carro cadastrado com sucesso
                carro=carro
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem='Erro: Esse carro ja foi cadastrado'
            )
        )

@app.route('/carros', methods=['DELETE'])
def delete_carro():
    carro = request.json # Capturando o carro da requisição em armazenando na variável carro
    modelo = carro.get('modelo') # Recebe o modelo do carro
    my_cursor = mydb.cursor()

    sql_check = "SELECT * FROM carros WHERE modelo = %s" # Busca todos os carros com o modelo especificado no banco de dados
    valores_check = (modelo,) # Armazena o modelo dentro de uma tupla. O uso da vírgula é para garantir que seja tratado como uma tupla de um único elemento
    my_cursor.execute(sql_check, valores_check) # Executa a consulta SQL com o modelo como parâmetro, de forma segura
    resultado = my_cursor.fetchall()

    if resultado: # Verifica se o modelo do carro foi encontrado
        delete_sql = "DELETE FROM carros WHERE modelo = %s" # Deleta na tabela carros, o carro do modelo passado na requisição
        values_delete = (modelo,) # Passa-se uma virgula, pois o MySQL Connector espera uma tupla. Quando passamos sem a virgula, o MySQL entende que é uma string normal

        my_cursor.execute(delete_sql, values_delete) # Executando o comando SQL de exclusão de dados
        mydb.commit()

        return make_response(
            jsonify(
                mensagem=f'Carro {modelo} excluído com sucesso.'
            )
        )
    else:
        return make_response(
            jsonify(
                mensagem=f'Carro {modelo} não encontrado'
            )
        )

@app.route('/carros', methods=['PUT'])
def update_carro():
    carro = request.json

    modelo = carro.get('modelo') # Recebe o modelo do carro
    ano = carro.get('ano') # Recebe o ano do carro
    my_cursor = mydb.cursor()

    sql_check = "SELECT * FROM carros WHERE modelo = %s" # Busca todos os carros com o modelo especificado no banco de dados
    valores_check = (modelo,) # Armazena o modelo dentro de uma tupla. O uso da vírgula é para garantir que seja tratado como uma tupla de um único elemento
    my_cursor.execute(sql_check, valores_check) # Executa a consulta SQL com o modelo como parâmetro, de forma segura
    resultado = my_cursor.fetchall()
    
    if resultado: # Verifica se o modelo do carro foi encontrado
        update_sql = "UPDATE carros SET ano = %s WHERE modelo = %s" # Atualiza na tabela carros, o ano e o modelo do carro
        values_update = (ano, modelo)

        my_cursor.execute(update_sql, values_update)
        mydb.commit()

        return make_response(
            jsonify(mensagem=f'Carro {modelo} atualizado com sucesso')
        )
    else:
        return make_response(
            jsonify(mensagem=f'Carro {modelo} não encontrado')
        )
    
app.run() # Rodando a API