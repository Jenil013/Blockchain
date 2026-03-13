from pymongo import MongoClient

# Connect to the MongoDB instance running in Docker
client = MongoClient('mongodb://admin:qwerty@localhost:27017', authSource='admin')

# Database and collections
db = client['blockchain_db']
transactions_collection = db['transactions']
blocks_collection = db['blocks']
