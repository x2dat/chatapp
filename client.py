import socketio
import tkinter as tk
from tkinter import simpledialog, scrolledtext

SERVER_URL = "wss://chatapp-jrvj.onrender.com"  # Use "wss://" for WebSockets

# Connect to the WebSocket server
sio = socketio.Client()

previous_sender = None  # To track the last message sender

def start_client(username):
    global previous_sender
    sio.connect(SERVER_URL)
    
    def send_message():
        global previous_sender
        message = entry.get()
        if message:
            sio.send(f"{username}: {message}")
            if previous_sender and previous_sender != username:
                chatbox.insert(tk.END, "\n" + "-" * 50 + "\n")
            chatbox.insert(tk.END, f"You: {message}\n")
            previous_sender = username
            entry.delete(0, tk.END)

    @sio.on("message")
    def receive_message(msg):
        global previous_sender
        sender = msg.split(": ")[0]  # Extract sender name
        if previous_sender and previous_sender != sender:
            chatbox.insert(tk.END, "\n" + "-" * 50 + "\n")
        chatbox.insert(tk.END, msg + "\n")
        previous_sender = sender

    # UI Setup
    root = tk.Tk()
    root.title(f"CMD Chat - {username}")
    root.configure(bg="black")

    chatbox = scrolledtext.ScrolledText(root, bg="black", fg="white", font=("Courier", 12), wrap=tk.WORD)
    chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(root, bg="black", fg="white", font=("Courier", 14))
    entry.pack(padx=10, pady=10, fill=tk.X)

    send_button = tk.Button(root, text="Send", command=send_message, bg="gray", fg="black", font=("Courier", 14), height=2)
    send_button.pack(pady=5, padx=10, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    username = simpledialog.askstring("Login", "Enter your username:")
    start_client(username)
