# Import the socket library to enable socket communication
import socket

# Import threading to enable concurrent receiving of messages
import threading

# Define server address and port to connect to
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

# Function to continuously receive and print messages from the server
def receive_messages(sock):
    while True:  # Infinite loop to constantly listen for messages
        try:
            message = sock.recv(1024).decode()  # Receive message from server and decode it
            if not message:  # If no message is received, the connection has closed
                break
            print("\n" + message)  # Print received message with newline for clarity
        except:
            print("🍃 Connection to the server has been lost.")
            break  # Break the loop if there's an error

# Main client function to connect and communicate with server
def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # Create a TCP/IP socket
        sock.connect((SERVER_HOST, SERVER_PORT))  # Connect socket to server address

        welcome_message = sock.recv(1024).decode()  # Receive initial welcome message from server
        print(welcome_message)  # Print welcome message to user

        panda_name = input("Enter your Panda Name: ")  # Prompt user to enter their unique panda name
        sock.send(panda_name.encode())  # Send the panda name to the server

        # Start thread to listen for incoming messages from the server without blocking input
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        while True:  # Infinite loop to allow continuous user input
            message = input()  # Get user's message input from console
            sock.send(message.encode())  # Send the user's message to the server

            if message == "@leaves":  # Special command to exit the chat room gracefully
                print("🍃 Leaving the Panda Chat Room... Goodbye! 🐼👋")
                break  # Exit the loop and terminate client

# Entry point to execute client when the script runs
if __name__ == "__main__":
    start_client()
