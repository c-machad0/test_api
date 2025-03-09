from flask import Flask, make_response, jsonify, request

Carros = [
    {
        'id': 1,
        'marca': 'Fiat',
        'modelo': 'Marea',
        'ano': 1999
    },
    {
        'id': 2,
        'marca': 'Fiat',
        'modelo': 'Uno',
        'ano': 1992
    },
    {
        'id': 3,
        'marca': 'Ford',
        'modelo': 'Escort',
        'ano': 1985
    },
    {
        'id': 4,
        'marca': 'Chevrolet',
        'modelo': 'Chevette',
        'ano': 1978
    },
    {
        'id': 5,
        'marca': 'Volkswagen',
        'modelo': 'Fusca',
        'ano': 1962
    },
]

app = Flask(__name__) # Instanciando variável e usando o nome do modulo como nome da API
app.config['JSON_SORT_KEYS'] = False # Para que o flask não ordene alfabeticamente as requisições enviadas

@app.route('/carros', methods=['GET'])
def get_carros(): # Criei uma função que retorna os carros e marquei a função para mostrar que é uma rota da API
    return make_response( # make_responsa ajuda a construir uma resposta de APIs
        jsonify(
            mensagem='Lista de carros.',
            dados=Carros
        ) # jsonify retorna a resposta em formato json (formato padrão de respostas de APIs)
    )

@app.route('/carros', methods=['POST'])
def create_carro():
    carro = request.json # Capturando o carro da requisição em armazenando na variável carro
    Carros.append(carro) # Adicionando o carro da requisição no banco dedados
    return make_response(
        jsonify(
            mensagem='Carro cadastrado com sucesso.',
            carro=carro
        )
    )

app.run() # Rodando a API