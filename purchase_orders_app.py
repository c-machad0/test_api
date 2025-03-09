from flask import Flask, jsonify, request

app = Flask(__name__) # Armazena nessa variavel o nome do arquivo

purchase_orders = [
    {
    'id': 1,
    'description': 'Pedido de de Compra 1',
    'items': [
        {
            'id': 1,
            'description': 'Item do pedido 1',
            'price': 20.99
        }
    ]
    }
]

# endpoints
# GET purchase_orders - retorna uma lista com os pedidos de compra
# GET purchase_orders_by_id - retorna uma lista com os pedidos de compra com um filtro por 'id'
# POST purchase_orders - inserir um novo pedido de compra
# GET purchase_orders_items - obter pedidos de um item especifico
# POST purchase_orders_items - inserir um pedido de item especifico

@app.route('/') # Informando que essa função será chamada quando a rota '/' for passada
def home():
    return 'API - Purchase Orders'

@app.route('/purchase_orders') # Retorna os pedidos de compras no formato json
def get_purchase_orders():
    return jsonify(purchase_orders)

@app.route('/purchase_orders/<int:id>') # Retorna o pedido de compra baseado no id do pedido
def get_purchase_orders_by_id(id):
    for index in purchase_orders:
        if index['id'] == id:
            return jsonify(index), 200 # Retorna o pedido de compra em formato json
    return jsonify(f'message: Pedido {id} não encontrado'), 404

@app.route('/purchase_orders', methods=['POST']) # Restringe esse endpoint para aceitar requisições POST apenas
def create_purchase_order(): # Função que vai adicionar pedidos na API
    request_data = request.get_json() # Variavel que vai armazenar a nova requisição de pedidos em formato json
    purchase_order = { # Novo pedido
        'id': request_data['id'], # Pega o valor do pedido digitado na requisição e relaciona com a chave 'id'
        'description': request_data['description'], # Pega o valor da descrição do pedido digitado na requisição e relaciona com a chave 'description'
        'items': []
    }

    purchase_orders.append(purchase_order) # Adiciona o novo pedido à lista de pedidos ja existente

    return jsonify(purchase_order) # Retorna o novo pedido em formato json

@app.route('/purchase_orders/<int:id>/items') # Retorna as especificações de cada item, de cada pedido de compra
def get_purchase_orders_items(id):
    for index in purchase_orders: # Itera sobre os pedidos de compra
        if index['id'] == id: # Compara o index com o pedido de compra recebido pela função
            return jsonify(index['items']), 200 # Retorna as especificações dos itens do pedido
    return jsonify(f'message: Pedido {id} não encontrado'), 404

@app.route('/purchase_orders/<int:id>/items', methods=['POST']) 
def create_purchase_orders_items(id):
    req_data = request.get_json()
    for index in purchase_orders: 
        if index['id'] == id:
            index['items'].append({
                'id': req_data['id'],
                'description': req_data['description'],
                'price': req_data['price']
            })
            return jsonify(index), 200 
    return jsonify(f'message: Pedido {id} não encontrado'), 404

app.run(port=5000) # Executar nossa aplicação na porta 5000