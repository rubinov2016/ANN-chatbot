import tkinter as tk
from tkinter import simpledialog

# Function to handle user input and generate a response (dummy function for demonstration)
def get_response(input_string):
    # Replace this with the logic of your chatbot
    return "You said: " + input_string

# Function to handle sending message
def send_message():
    user_input = text_entry.get()
    response = get_response(user_input)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.insert(tk.END, "Bot: " + response + "\n")
    text_entry.delete(0, tk.END)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Chatbot")

# Chat history text box
chat_history = tk.Text(root, height=15, width=50)
chat_history.pack()

# Text entry box for user input
text_entry = tk.Entry(root, width=50)
text_entry.pack()

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Run the GUI loop
root.mainloop()
