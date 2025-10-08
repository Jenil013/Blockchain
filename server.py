from flask import Flask, jsonify, request 
from Blockchain import Blockchain
from uuid import uuid4  
import hashlib
import json
from textwrap import dedent  

from flask import render_template

#Instantiating the app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('blockchain_frontend.html')

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#Instantiating the Blockchain 
blockchain = Blockchain()


@app.route('/mine', methods = ['GET'])
def mine():
    #calculate the proof of work
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    #rewarding the miner, considering 0 as a system'

    blockchain.new_transaction(sender = "0", recipient = node_identifier, amount = 1)

    #forge the new block by adding to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': 'New Block Forged', 
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']

    }
    return jsonify(response), 200




@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    
    values = request.get_json()

    #check all the requirements are met 
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400
    
    #create a new transaction 
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added at {index}'}

    return jsonify(response), 201





@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

@app.route('/nodes/register', methods = ['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please input the valid list of nodes", 200
    
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'Message': "The nodes have been registered successfully", 
        'Total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 201

@app.route('/node/resolve', methods = ['GET'])
def consensus():

    resolve = blockchain.resolve_conflicts()

    if resolve:
        response = {
            'message': "Our chain was replaced", 
            'new-chain': blockchain.chain
        }

    else:
        response = {
            'message': "Chain was Authoritative.",
            'chain': blockchain.chain
        }

    return jsonify(response), 200



if __name__ == '__main__':
    import sys
    
    # Default port
    port = 5000
    
    # Check for --port argument
    if '--port' in sys.argv:
        port_index = sys.argv.index('--port')
        if port_index + 1 < len(sys.argv):
            port = int(sys.argv[port_index + 1])
    
    app.run(host='0.0.0.0', port=port, debug=True)
