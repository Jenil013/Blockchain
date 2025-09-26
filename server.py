from flask import Flask
import Blockchain
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
    return "We will mine a new Block"


@app.route('/transaction/new', methods = ['POST'])
def new_transaction():
    return "We will add a new transaction"

@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }

    return jsonify(response), 200


if __name__ == 'main':
    app.run(host = '0.0.0.0' , post = 5000)