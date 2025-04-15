# Haroon Ahmad
# ECE 146 - Hovannes Kulhandjian
# 04/23/2025

import socket
import threading

IP_ADDR = ""
PORT = 9876

clients = []

def send_full_message(send_message, client_socket):
    # Send a message to a client. First sends the length of the message then the message itself
    send_message_length = len(send_message.encode())
    client_socket.send(str(send_message_length).zfill(10).encode())
    client_socket.send(str.encode(send_message))

def broadcast_message(message, current_client):
    # Send the message to all other clients except the one that sent the message
    for client in clients:
        if client != current_client:
            send_full_message(message, client)

def recv_full_message(client_socket):
    while True:
        try:
            client_info = str(client_socket.getpeername())
            # Recieve the message length first
            message_length = int(client_socket.recv(10).decode())
            recv_message = b""

            # Keep extracting the messsage until the entire message has been compiled
            while len(recv_message) < message_length:
                chunk_size = min(2048, message_length - len(recv_message))
                chunk = client_socket.recv(chunk_size)
                recv_message += chunk

            recv_message = recv_message.decode().strip()

            # If client exited chatroom, begin removing the client
            if recv_message == "exit()":
                raise Exception
            # Print the message and broadcast it to all other clients
            print(f"Client {client_info}: ", recv_message)
            broadcast_message(f"Client {client_info}: {recv_message}", client_socket)

        except Exception as e: # Connection broke
            
            exit_message = f"{client_info} left the chat!"
            # Print and broadcast exit message. Remove client from server and close its connection
            print(exit_message)
            broadcast_message(exit_message, client_socket)
            clients.remove(client_socket)
            client_socket.close()
            break

def handle_client(server_socket):

    # Wait for incoming connections to come in 
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {str(addr)}")

        clients.append(client_socket)
        # Send conformation message to client
        client_socket.send(str.encode("Connection successfull"))
        broadcast_message(f"{str(addr)} has joined!", client_socket)

        # Start thread to listen for the client's incoming messages
        t = threading.Thread(target=recv_full_message, args=(client_socket,))
        t.start()

def shutdown_server(s):
    print("Shutting down server...")

    # Go through each client, send a shutdown message, then close the connection.
    for client in clients:
        try:
            send_full_message("Server is shutting down.", client)
            client.close()
        except Exception as e:
            print(f"Error closing client socket: {e}")

    clients.clear()
    # Close the server socket
    s.close()
    print("Server has been shut down.")

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP_ADDR, PORT))
        s.listen()
        print("Waiting for a connection...")

        # Client handling is in another thread so main thread can wait for exit command
        server_thread = threading.Thread(target=handle_client, args=(s,), daemon=True)
        server_thread.start()

        while True:
            cmd = input()
            if cmd.strip() == "exit()":
                shutdown_server(s)
                break
    except KeyboardInterrupt:
    # Server will shut down gracefully is user forces a shutdown
        shutdown_server(s)

if __name__ == "__main__":
    main()