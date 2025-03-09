from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
    'id': 1,
    'description': 'Ir para academia'
    }
]
# Função que retorna o ID solicitado e assim que é encontrado, a iteração para
def get_task_by_id(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)

@app.route('/')
def home():
    return 'To-do-list API'

@app.route('/tasks')
def get_tasks():
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_tasks():
    # Verifica se a requisição está em JSON
    if not request.is_json:
        return jsonify({'message': 'Requisição deve ser em JSON'}), 400

    request_task = request.get_json()
    description = request_task.get('description')

    # Verificar se a requisição foi escrita
    if not description or len (description) < 3:
        return jsonify({'message': 'Descrição é obritatória e deve ser maior que 3 caracteres'})
    
    # Verifica se ja existe a descrição
    if any(task['description'] == description for task in tasks):
        return jsonify({'message': f'A tarefa {description} já existe.'}), 400

    # Verifica o maior numero de id existente e incrementa 1, gerando o proximo id
    new_id = max([task['id'] for task in tasks], default=0) + 1
    new_task = {
        'id': new_id,
        'description': description
        }
        
    tasks.append(new_task)

    return jsonify(new_task), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = get_task_by_id(id)
    if not task:
        return jsonify({'message': f'Tarefa {id} não encontrada.'}), 404
    
    if not request.is_json:
            return jsonify({'message': 'Descrição é obritatória e deve ser maior que 3 caracteres'}), 400

    request_task = request.get_json()
    description = request_task.get('description')

    if description:
        if len(description) < 3:
            return jsonify({'message': 'Descrição é obritatória e deve ser maior que 3 caracteres'}), 400
        # Verifica se existe a mesma descrição dentre todas as tarefas
        if any(t['description'] == description and t['id'] != id for t in tasks):
            return jsonify({'message': f'A descrição {description} já está em uso.'}), 400
        task['description'] = description
    
    return jsonify(task), 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = get_task_by_id(id)
    if not task:
        return jsonify({'message': f'Tarefa {id} não encontrada.'}), 404
    
    tasks.remove(task)
    return jsonify({'message': f'Tarefa {id} foi removida.'}), 200

app.run(port=5000)