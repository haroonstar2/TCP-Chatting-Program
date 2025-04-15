
# TCP Chatting Program

A basic TCP-based client-server chat application built in Python using sockets and threading.

This project is a basic multi-client chat server and client application built with Python using sockets and threading. The server handles multiple client connections, relays messages between users, and supports graceful shutdown. Clients can connect, send and receive messages, and exit the chat with a simple command-line interface.

---

## Features

- Multi-client support using threads
- Real-time message broadcasting
- Graceful client and server shutdown
- No third-party libraries required (built-in only)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/haroonstar2/TCP-Chatting-Program.git
```

Navigate to the project directory:

```bash
cd TCP-Chatting-Program
```

---

## Usage

**1. Start the Server**

In one terminal window:

```bash
python server.py
```

**2. Start the Client**

In separate terminal windows (you can open multiple to simulate different users):

```bash
python client.py
```

Each client will connect to the server and can begin chatting.

---

## Notes

- **Start the server before launching any clients**
- **To exit the chat, type `exit()` and press Enter**
- Tested with Python 3.11.2 on Windows 11

---

## License

This project is for educational use (ECE 146: Computer Networks @ CSU Fresno). Feel free to modify or build on it.
