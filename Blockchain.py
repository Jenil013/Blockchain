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

    def new_block(self, proof, previous_hash = None):
        """
        Creates a new block and adds it to the chain.

        Parameters:
            proof (int): The proof given by the Proof of Work algorithm.
            previous_hash (str, optional): Hash of previous Block. Defaults to None.

        Returns:
            dict: New Block
        """
        pass

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
        pass

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

        pass

