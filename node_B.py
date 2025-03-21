import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate RSA key pair for B
private_key_B = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key_B = private_key_B.public_key()

# Serialize B's public key to send to A
serialized_public_key_B = public_key_B.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Function to handle receiving messages
def receive_messages():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 6000))  # B listens on port 6000
    server.listen(1)
    print("B is listening on port 6000...")

    conn, _ = server.accept()
    print("Connected to A")

    # Receive A's public key
    serialized_public_key_A = conn.recv(4096)
    public_key_A = serialization.load_pem_public_key(serialized_public_key_A)

    # Send B's public key to A
    conn.sendall(serialized_public_key_B)

    # Receive encrypted message from A
    encrypted_message = conn.recv(4096)

    # Decrypt the received message
    decrypted_message = private_key_B.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print(f"B received and decrypted: {decrypted_message.decode()}")
    conn.close()
    server.close()

# Function to send messages
def send_message():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))  # Connect to A's server (port 5000)

    # Send B's public key to A
    client.sendall(serialized_public_key_B)

    # Receive A's public key
    serialized_public_key_A = client.recv(4096)
    public_key_A = serialization.load_pem_public_key(serialized_public_key_A)

    # Encrypt message for A
    message = "I am sharing my Password with you : #gyhbuytdiuysiud1@7875hbyurf#"
    encrypted_message = public_key_A.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send encrypted message to A
    client.sendall(encrypted_message)
    client.close()

# Run receiver and sender in parallel
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_message).start()
