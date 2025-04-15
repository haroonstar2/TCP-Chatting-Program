# Haroon Ahmad
# ECE 146 - Hovannes Kulhandjian
# 04/23/2025

import socket
import threading
import sys

IP_ADDR = "localhost"
PORT = 9876

def send_full_message(sock):
    while True:
        send_message = input("").strip()
        # Prevents sending empty messages
        if not send_message:
            print("Please enter a non-empty message")
            continue
        # Send message length to server first
        send_message_length = len(send_message.encode())
        try:
            sock.send(str(send_message_length).zfill(10).encode())
            sock.send(str.encode(send_message))
        except:
            print("Server shut down unexpectedly")
            close_connection(sock)
            break
        # If exit command is typed
        if send_message == "exit()":
            print("Client ended the chat.")
            close_connection(sock)

def recv_full_message(sock):
    while True:
        try:
            message_length = int(sock.recv(10).decode())
            
            if not message_length:
                print("Server closed the connection.")
                close_connection(sock)

            recv_message = b""
            while len(recv_message) < message_length:
                chunk = sock.recv(min(2048, message_length - len(recv_message)))
                if not chunk:
                    print("Server disconnected.")
                    close_connection(sock)    
                recv_message += chunk

            recv_message = recv_message.decode().strip()

            # If exit command is typed
            if recv_message == "exit()" or recv_message == "Server is shutting down.":
                print("Server ended the chat.")
                close_connection(sock)
                break

            print(recv_message)
            
        except Exception as e:
            close_connection(sock)
            break

def close_connection(sock):
    sock.close()
    sys.exit()

def main():

    # Create socket using IPv4 and TCP protocols
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server ip_addr and port
    try:
        s.connect((IP_ADDR, PORT))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()

    # Recieve conformation message
    recv_message = s.recv(2048)
    print("Recieved:", recv_message.decode())

    # Start thread to recieve messages
    threading.Thread(target=recv_full_message, args=(s,)).start()

    # Start send message loop
    send_full_message(s)

if __name__ == "__main__":
    main()