from urllib.parse import urlparse
from blake3 import blake3
import json
import requests
from datetime import datetime
from db_config import transactions_collection, blocks_collection


class Blockchain(object):
    """
    ---------------------------------------------------------------------------------------
    A simple Blockchain class responsible for managing the chain and transactions.
    ---------------------------------------------------------------------------------------

    Attributes:
        chain (list): A list to store the blockchain.
        current_transaction (list): A list to store the current transactions.

    ---------------------------------------------------------------------------------------
    Methods:
        new_block(): Creates a new block and adds it to the chain.
        new_transaction(): Adds a new transaction to the list of transactions.
        hash(block): Creates a SHA-256 hash of a block.
        last_block(): Returns the last block in the chain.
    
    """
    def __init__ (self):
        self.chain = []
        self.current_transaction = []
        self.nodes = set()

        # Load existing chain from MongoDB, or create genesis block
        saved_blocks = list(blocks_collection.find({}, {'_id': 0}).sort('index', 1))
        if saved_blocks:
            self.chain = saved_blocks
        else:
            self.new_block(proof = 100, previous_hash = '1')


    def new_block(self, proof, previous_hash = None):
        """
        Creates a new block and adds it to the chain.

        Parameters:
            proof (int): The proof given by the Proof of Work algorithm.
            previous_hash (str, optional): Hash of previous Block. Defaults to None.

        Returns:
            dict: New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'transactions': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        #empting the current transcation
        self.current_transaction = []

        self.chain.append(block)

        # Persist block to MongoDB
        blocks_collection.insert_one(dict(block))

        return block
    



    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        Parameters:
            sender (str): Address of the Sender
            recipient (str): Address of the Recipient
            amount (float): Amount

        Returns:
            int: The index of the Block that will hold this transaction
        """
        
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.current_transaction.append(transaction)

        # Persist transaction to MongoDB
        block_index = self.last_block['index'] + 1
        db_record = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'block_index': block_index,
            'timestamp': datetime.utcnow().isoformat()
        }
        transactions_collection.insert_one(db_record)

        #indicating the new index in block
        return block_index
    

    @staticmethod   
    def hash(block):
        # Creates a SHA-256 hash of a Block
        """
        Creates a BLAKE3 hash of a Block 

        Params: 
            block (dict): Block

        Returns:
            str: The hash of the block in hexadecimal format.       
        """

        block_string = json.dumps(block, sort_keys = True).encode()

        return blake3(block_string).hexdigest()


    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
        

    @staticmethod
    def valid_proof(last_proof, proof):

        guess = f"{last_proof}{proof}".encode()
        hash = blake3(guess).hexdigest()
        return hash[:4] == "1234"
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) != True:
            proof += 1

        return proof
    
    #Registering new nodes into Blockchain
    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    #check whether the chain is valid or not 
    def valid_chain(self, chain):

        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1 

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            
            if block['previous_hash'] != self.hash(last_block): # Check that the hash of the last block is correct
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):   # Check that the Proof of Work is correct
                return False
            
            last_block = block
            current_index += 1 

        return True

#Consensus Algorithm to resolve conflicts between blockchain nodes.
    def resolve_conflicts(self):
        
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """ 
        
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

            if max_length < length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
                        
            

        if new_chain:
            self.chain = new_chain
            return True 

        return False



