# 🔗 Blockchain in Python 

> A lightweight, educational blockchain implemented in Python with a small Flask API. Perfect for learning how blocks, transactions, and proof-of-work fit together.  

>By Jenil Patel & Khushbu Talaviya

---

&#x20;&#x20;

---

## 🎯 Project Overview

This repository implements a *minimal* blockchain (blocks, transactions, proof-of-work) and exposes a tiny HTTP API built with Flask so you can mine blocks, add transactions, and inspect the chain.

> Source reference: server endpoints and API logic are implemented in `server.py` and blockchain internals are in `Blockchain.py`.

---

## 🔍 What makes this README "interactive"?

- Clear, copy-paste command examples (curl & Python) so you can try the API immediately.
- Postman examples to import and play with the API visually.
- Endpoint request/response examples so you can paste into your terminal or REST client.
- Troubleshooting tips and quick debugging checklist.

---

## 📁 Project structure (quick)

- `server.py` — small Flask web server exposing endpoints to interact with the chain.
- `Blockchain.py` — core blockchain class (blocks, transactions, BLAKE3 hashing, proof-of-work).
- `README.md` — (you’re looking at it)

---

## ⚡ Quick start (run locally)

**Requirements**

- Python 3.10+
- Create and activate a venv

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install minimal dependencies directly:

```bash
pip install Flask blake3
```

**Run the server**

```bash
python server.py
```

> If nothing happens, make sure the `if __name__ == '__main__':` guard is spelled correctly in `server.py`. (Common bug: `if __name__ == 'main':` will **not** start the app.)

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

---

## 🧠 Implementation details & highlights

- The blockchain uses **BLAKE3** for hashing (see `Blockchain.hash`).
- Proof-of-work uses a simple check where the hex digest of `blake3(str(last_proof)+str(proof))` must start with `"1234"`.
- Mining rewards are granted by adding a transaction with `sender = "0"` and `recipient = <node id>`.

> For exact implementation you can inspect `Blockchain.py` and `server.py`.

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

## 🧪 Tests & Development

- Add unit tests for `Blockchain.new_block`, `new_transaction`, `hash`, `proof_of_work`, and `valid_proof`.
- Consider adding a small `tests/` folder and run with `pytest`.

---


## ✅ Contribution guide

- Fork the repo, create a feature branch, open a PR.
- Use clear commit messages and add unit tests for behavior changes.

---


