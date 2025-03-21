import socket
import pickle
import threading
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes

private_key_A = rsa.generate_private_key(public_exponent= 65537 , key_size=2048)
public_key_A = private_key_A.public_key()

serialized_public_key_A = public_key_A.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def receive_messages():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1",5000))
    server.listen(1)
    print("Server initiated connected at port 5000")
    conn,_ = server.accept()
    serialized_public_key_B = conn.recv(4096)
    public_key_B = serialization.load_pem_public_key(serialized_public_key_B)
    conn.sendall(serialized_public_key_A)
    encrypted_message = conn.recv(4096)
    decrypted_message = private_key_A.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"A received and decrypted: {decrypted_message.decode()}")
    conn.close()
    server.close()

def send_message():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 6000))  # Connect to B's server (port 6000)

    # Send A's public key to B
    client.sendall(serialized_public_key_A)

    # Receive B's public key
    serialized_public_key_B = client.recv(4096)
    public_key_B = serialization.load_pem_public_key(serialized_public_key_B)

    # Encrypt message for B
    message = "Hi please fetch My password as : Qutvdxeopis@3vhbd$u8&&09"
    encrypted_message = public_key_B.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send encrypted message to B
    client.sendall(encrypted_message)
    client.close()

# Run receiver and sender in parallel
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_message).start()