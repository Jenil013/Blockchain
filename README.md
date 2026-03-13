# 🔗 Blockchain in Python 

> A lightweight, educational blockchain implemented in Python with Flask and MongoDB. Features blocks, transactions, proof-of-work, consensus, and persistent storage via MongoDB.  

>By Jenil Patel & Khushbu Talaviya

---

&#x20;&#x20;

---

## 🎯 Project Overview

This repository implements a *minimal* blockchain (blocks, transactions, proof-of-work) and exposes a tiny HTTP API built with Flask so you can mine blocks, add transactions, and inspect the chain.

> Source reference: server endpoints and API logic are implemented in `server.py` and blockchain internals are in `Blockchain.py`.

---

## 📁 Project structure (quick)

- `server.py` — small Flask web server exposing endpoints to interact with the chain.
- `Blockchain.py` — core blockchain class (blocks, transactions, BLAKE3 hashing, proof-of-work).
- `README.md` — (you’re looking at it)
- `blockchain_frontend.html` — Frontend for the app

---

## 🖼️ Home Page Preview

![Blockchain Manager Home Page](https://github.com/Jenil013/Blockchain/blob/main/Homepage.png)

---

## ⚡ Quick start (run locally)

**Requirements**

- Python 3.10+
- Docker (for MongoDB and Mongo Express)

**1. Start MongoDB and Mongo Express with Docker**

```bash
# Start MongoDB
docker run -d --name mongodb -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=qwerty \
  mongo

# Start Mongo Express (web UI for MongoDB)
docker run -d --name mongo-express -p 8081:8081 \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=pass \
  -e ME_CONFIG_MONGODB_URL=mongodb://admin:qwerty@host.docker.internal:27017/ \
  mongo-express
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

**Run the server**

```bash
python server.py
```

---

## 🧭 API Endpoints (try these)

### 1) Mine a new block

```
GET /mine
```

Response (success): 200 OK

```json
{
  "message": "New Block Forged",
  "index": 2,
  "transactions": [],
  "proof": 35293,
  "previous_hash": "..."
}
```

**curl**

```bash
curl -X GET http://127.0.0.1:5000/mine
```

### 2) Add a new transaction

```
POST /transaction/new
Content-Type: application/json
Body: { "sender": "address1", "recipient": "address2", "amount": 5 }
```

Response (success): 201 Created

```json
{ "message": "Transaction will be added at 3" }
```

**curl**

```bash
curl -X POST http://127.0.0.1:5000/transaction/new \
  -H "Content-Type: application/json" \
  -d '{"sender":"alice","recipient":"bob","amount":2}'
```

### 3) View the full blockchain

```
GET /chain
```

Response: 200 OK

```json
{
  "chain": [ ... ],
  "length": 4
}
```

**curl**

```bash
curl -X GET http://127.0.0.1:5000/chain
```

### 4) View all transactions (from MongoDB)

```
GET /transactions
```

Response: 200 OK

```json
{
  "transactions": [
    {
      "sender": "alice",
      "recipient": "bob",
      "amount": 5,
      "block_index": 2,
      "timestamp": "2026-03-12T23:28:18.000000"
    }
  ],
  "count": 1
}
```

**curl**

```bash
curl -X GET http://127.0.0.1:5000/transactions
```

---

## 🧠 Implementation details & highlights

- The blockchain uses **BLAKE3** for hashing (see `Blockchain.hash`).
- Proof-of-work uses a simple check where the hex digest of `blake3(str(last_proof)+str(proof))` must start with `"1234"`.
- Mining rewards are granted by adding a transaction with `sender = "0"` and `recipient = <node id>`.

> For exact implementation, you can inspect `Blockchain.py` and `server.py`.

---

## 🗄️ MongoDB Persistence

All blockchain data is persisted to a **MongoDB** database (`blockchain_db`) running in Docker, ensuring that the chain and transactions survive server restarts.

| Collection     | Description                                                          |
| -------------- | -------------------------------------------------------------------- |
| `blocks`       | Stores every block (index, proof, previous_hash, transactions).      |
| `transactions` | Stores every transaction (sender, recipient, amount, timestamp).     |

**How it works:**

- On **server startup**, the `Blockchain` class checks MongoDB for existing blocks. If found, the chain is loaded from the database. Otherwise, a fresh genesis block is created.
- When a **new block is mined**, it is appended to the in-memory chain *and* inserted into the `blocks` collection.
- When a **new transaction is created**, it is added to the pending transactions *and* inserted into the `transactions` collection with a UTC timestamp.

**Mongo Express** is available at `http://localhost:8081` to browse the stored data visually.

---

## ⚖️ Consensus Algorithm (Resolving Conflicts)

The blockchain implements a simple consensus mechanism known as Longest Chain Rule to ensure all nodes remain in agreement.

Each node keeps its own version of the chain. When a conflict occurs (e.g., another node’s chain differs), the algorithm:

**1.** Requests the /chain endpoint from all registered nodes.

**2.** Validates each chain by checking that every block’s previous_hash matches the hash of the block before it and that proofs of work are valid.

**3.** Replaces its own chain with the longest valid chain found.

This ensures the network always agrees on a single, most credible chain.

---

## 📦 Postman / Insomnia

Create a simple collection with the three endpoints above. Example Postman body for `POST /transaction/new`:

```json
{
  "sender": "Jenil",
  "recipient": "Khushbu",
  "amount": 10
}
```

---

## ✅ Contribution guide

- Fork the repo, create a feature branch, open a PR.
- Use clear commit messages and add unit tests for behavior changes.

---


