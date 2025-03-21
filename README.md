# 🔐 Asymmetric Encryption-Based Communication

This project demonstrates **end-to-end encrypted communication** between two endpoints (A & B) using **asymmetric encryption (RSA)** and **socket programming** in Python. Each endpoint generates its own public-private key pair, exchanges public keys, and encrypts/decrypts messages securely.

---

## 🚀 Features
- **RSA Key Pair Generation**: Each endpoint generates its own keys.
- **Public Key Exchange**: Endpoints share public keys.
- **Message Encryption & Decryption**: Messages are encrypted with the recipient's **public key** and decrypted with the recipient's **private key**.
- **Secure Communication over TCP Sockets**.

---

## 🛠️ How It Works
1. **A & B generate RSA key pairs (public & private).**
2. **They exchange public keys.**
3. **A encrypts a message using B’s public key.**
4. **B decrypts the message using its private key.**
5. **B sends a response using A’s public key, and A decrypts it.**

---

## 📌 Installation & Setup
### **1️⃣ Install Dependencies**
Make sure Python 3 is installed, then install the required module:
```sh
pip install cryptography
