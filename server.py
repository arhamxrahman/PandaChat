# Panda Chat Room Server
import socket  # Library for networking
import threading  # Enables concurrency (handling multiple clients simultaneously)
import random  # Used for random selection of panda-themed emojis and facts
import logging  # Used to keep a log of server activity

# Server configuration
HOST = 'localhost'  # Server IP address (localhost for local testing)
PORT = 12345  # Server port to listen for incoming connections

# Panda-themed data
PANDA_EMOJIS = ["🐼", "🎋", "🌿", "🍃", "🎍"]  # Emojis for decoration
PANDA_FACTS = [  # List of panda-related facts for @bamboo command
    "Pandas spend around 14 hours a day eating bamboo!",
    "Baby pandas are pink and weigh only 100 grams!",
    "A group of pandas is called an embarrassment!",
    "Pandas are excellent tree climbers!",
    "Only around 1,800 giant pandas are left in the wild!"
]

# Lists to store connected clients and their panda-names
clients = []  # Store active client sockets
client_names = {}  # Map client sockets to panda names

# Function to broadcast messages to all connected clients, excluding sender if specified
def broadcast(message, sender_socket=None):
    for client in clients:  # Loop through connected clients
        if client != sender_socket:  # Exclude sender from broadcast if provided
            try:
                client.send(message.encode())  # Send message to client
            except:  # If sending fails, remove the disconnected client
                clients.remove(client)
                client.close()

# Function to handle an individual client's messages and interactions
def handle_client(client_socket):
    try:
        panda_name = client_names[client_socket]  # Retrieve client's panda name
        broadcast(f"🐼 {panda_name} has joined the Panda Chat Room! 🌿")  # Notify others of new user

        while True:  # Continuously listen for incoming messages from client
            message = client_socket.recv(1024).decode()  # Receive message from client

            if message == "@bamboo":  # Handle special panda fact command
                fact = random.choice(PANDA_FACTS)  # Select random panda fact
                client_socket.send(f"🎍 Panda Fact: {fact}".encode())  # Send fact to requester

            elif message == "@grove":  # Command to list connected pandas
                names_list = ', '.join(client_names.values())  # Gather names of all pandas
                client_socket.send(f"🌿 Pandas in Grove: {names_list}".encode())  # Send list to requester

            elif message == "@leaves":  # Command to gracefully disconnect
                client_socket.send("🍃 You are leaving the Panda Chat. Goodbye! 🐼".encode())
                broadcast(f"🍃 {panda_name} has left the Panda Chat.", client_socket)
                break  # Exit loop to disconnect client

            else:
                # Normal message broadcasting with random emoji decoration
                decorated_message = f"{random.choice(PANDA_EMOJIS)} {panda_name}: {message}"
                broadcast(decorated_message, client_socket)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(client_socket)  # Remove socket from active client list
        del client_names[client_socket]  # Remove client's panda name from dictionary
        client_socket.close()  # Close socket connection

# Main server function to start server and accept new connections
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))  # Bind server to specified host and port
        server_socket.listen()  # Begin listening for connections

        print(f"Panda Chat Server running at {HOST}:{PORT} 🐼")
        
        while True:  # Continuously accept new clients
            client_socket, client_address = server_socket.accept()  # Accept new client connection
            clients.append(client_socket)  # Add client socket to clients list

            # Request and receive panda name from the connected client
            client_socket.send("🐼 Welcome to Panda Chat Room! Enter your Panda Name:".encode())
            panda_name = client_socket.recv(1024).decode()
            client_names[client_socket] = panda_name  # Map socket to panda name

            # Start a new thread to handle client communication
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.daemon = True  # Daemon thread closes automatically upon main thread exit
            thread.start()

# Entry point of server script
if __name__ == "__main__":
    import threading  # Threading module for concurrent client handling
    import random     # Random module for random emoji/fact selection

    print("🐼 Panda Chat Server is starting...")
    start_server()  # Start server operation
