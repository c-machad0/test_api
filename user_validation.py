from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
    'id': 1,
    'nome': 'Luiz',
    'email': 'luizdev123@hotmail.com'
    }
]

@app.route('/')
def home():
    return 'API User Validation'

@app.route('/users')
def get_user():
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    request_user = request.get_json()
    new_user = {
        'id': request_user['id'],
        'nome': request_user['nome'],
        'email': request_user['email']
    }

    users.append(new_user)

    return jsonify(new_user), 201

@app.route('/users/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    request_user = request.get_json()

    for user in users:
        if user['id'] == id_user:
            user['nome'] = request_user.get('nome', user['nome'])
            user['email'] = request_user.get('email', user['email'])
            return jsonify(user), 200

    return jsonify({'message': f'Usuário {id_user} não encontrado'}), 404   

@app.route('/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    for user in users:
        if user['id'] == id_user:
            users.remove(user)
            return jsonify({'message': f'Usuario {id_user} foi removido com sucesso'}), 200
    
    return jsonify({'message': f'Usuario {id_user} não foi encontrado'})    
app.run(port=5000)