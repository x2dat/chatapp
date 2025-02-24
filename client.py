import socketio
import tkinter as tk
from tkinter import simpledialog, scrolledtext

SERVER_URL = "https://chatapp-jrvj.onrender.com"  # Your Render server URL

# Connect to the WebSocket server
sio = socketio.Client()

def start_client(username):
    sio.connect(SERVER_URL)
    
    def send_message():
        message = entry.get()
        if message:
            sio.send(f"{username}: {message}")
            chatbox.insert(tk.END, f"You: {message}\n")
            entry.delete(0, tk.END)

    @sio.on("message")
    def receive_message(msg):
        chatbox.insert(tk.END, msg + "\n")

    # UI Setup
    root = tk.Tk()
    root.title(f"CMD Chat - {username}")
    root.configure(bg="black")

    chatbox = scrolledtext.ScrolledText(root, bg="black", fg="green", font=("Courier", 12))
    chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(root, bg="black", fg="green", font=("Courier", 12))
    entry.pack(padx=10, pady=10, fill=tk.X)

    send_button = tk.Button(root, text="Send", command=send_message, bg="black", fg="green")
    send_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    username = simpledialog.askstring("Login", "Enter your username:")
    start_client(username)
