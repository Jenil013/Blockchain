from blake3 import blake3
import json


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

        #create the genesis block
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
        
        self.current_transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        #indicating the new index in block
        return self.last_block['index'] + 1
    

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



