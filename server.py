from flask import Flask, jsonify, request    
from blockchain import Blockchain
from uuid import uuid4  
import hashlib
import json
from textwrap import dedent  

#Instantiating the app
app = Flask(__name__)

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




@app.route('/transaction/new', methods = ['POST'])
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


if __name__ == 'main':
    app.run(host = '0.0.0.0' , port = 5000)
