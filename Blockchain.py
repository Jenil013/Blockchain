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

    def new_block(self):
        # Creates a new Block and adds it to the 
        pass

    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass

    @staticmethod
    def hash(block):
        # Creates a SHA-256 hash of a Block
        pass


    @property
    def last_block(self):
        # Returns the last Block in the chain

        pass

