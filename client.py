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
        # Gather user input
        send_message = input("").strip()
        # Prevents sending empty messages
        if not send_message:
            print("Please enter a non-empty message")
            continue
        # Send message length to server first then actual message to server
        send_message_length = len(send_message.encode())
        try:
            sock.send(str(send_message_length).zfill(10).encode())
            sock.send(str.encode(send_message))
        except:
        # Client could not send data to server. Initialize client shutdown
            print("Server shut down unexpectedly")
            close_connection(sock)
            break
        # If exit command is typed
        if send_message == "exit()":
            print("Client ended the chat.")
            close_connection(sock)

# Receving full message from the server
def recv_full_message(sock):
    while True:
        try:
            # Recieve message length
            message_length = int(sock.recv(10).decode())
            # Server did not send anything to the client
            if not message_length:
                print("Server closed the connection.")
                close_connection(sock)

            # Keep receiving data from server until full message is constructed
            recv_message = b""
            while len(recv_message) < message_length:
                chunk = sock.recv(min(2048, message_length - len(recv_message)))
                # Client could not properly recieve data from server
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

# Close the client and exit the program
def close_connection(sock):
    sock.close()
    sys.exit()

def main():

    # Create socket using IPv4 and TCP protocols
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server IP_ADDR and PORT
    try:
        s.connect((IP_ADDR, PORT))
    except Exception as e:
    # Catch any issues and exit the client
        print(f"Error: {e}")
        sys.exit()

    # Recieve conformation message from server
    recv_message = s.recv(2048)
    print("Recieved:", recv_message.decode())

    # Start thread to recieve messages
    threading.Thread(target=recv_full_message, args=(s,)).start()

    # Start send message loop
    send_full_message(s)

if __name__ == "__main__":
    main()