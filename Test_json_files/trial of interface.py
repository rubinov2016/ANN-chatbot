import tkinter as tk
from Test_json_files.chatbot import chat


class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("World Cup 2022")

        # Create and configure the chat history text widget
        self.chat_history = tk.Text(master, wrap=tk.CHAR, width=80, height=40, state=tk.DISABLED)
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Create an entry widget for user input
        self.entry = tk.Entry(master, width=40)
        self.entry.grid(row=1, column=0, padx=20, pady=20)

        # Create a button to trigger the chat function
        self.chat_button = tk.Button(master, text="Send", command=self.chat)
        self.chat_button.grid(row=1, column=1, padx=40, pady=40)
        self.entry.focus()

        # Bind the Enter key to the chat method
        self.entry.bind('<Return>', lambda event=None: self.chat())

        # text widget
        self.text_widget = tk.Text(master, wrap=tk.CHAR, width=20, height=20, state=tk.DISABLED)
        self.text_widget.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)
        # scroll bar
        scrollbar = tk.Scrollbar(self.text_widget)
        scrollbar.grid(row=4, column=2, sticky='ns')
        scrollbar.configure(command=self.text_widget.yview)

    def chat(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return  # User input is empty

        # Chatbot response
        chat_history_text = chat(user_input)

        # Update chat history
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, chat_history_text)
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

        # Update text widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"You: {user_input}\n  bot: {chat_history_text}\n\n")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.see(tk.END)

        # Clear the entry widget after processing user input
        self.entry.delete(0, tk.END)
        # Ensure the focus remains on the entry widget
        self.entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()
