import tkinter as tk
from tkinter import messagebox, scrolledtext
from SecurePasswordGenerator import SecurePasswordGenerator

class Window:
    def __init__(self, root):
        self.m_Root = root
        self.m_Root.title("Secure Password Generator")
        self.m_Root.geometry("700x600")  # Set the window size to be wider and taller

        self.CreateWidgets()

    def CreateWidgets(self):
        # Define font
        title_font = ("Cascadia Code", 16, "bold")
        label_font = ("Cascadia Code", 10, "bold")
        button_font = ("Cascadia Code", 10, "bold")

        # Create and place widgets
        frame = tk.Frame(self.m_Root, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        title_label = tk.Label(frame, text="Secure Password Generator", font=title_font)
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Password Length (12-25):", font=label_font).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.m_EntryLength = tk.Entry(frame, font=label_font)
        self.m_EntryLength.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Number of Passwords:", font=label_font).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.m_EntryCount = tk.Entry(frame, font=label_font)
        self.m_EntryCount.grid(row=2, column=1, pady=5)

        self.m_VarIncludeSpecial = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Include Special Characters", variable=self.m_VarIncludeSpecial, font=label_font).grid(row=3, column=0, columnspan=2, pady=5)

        self.m_VarExcludeSimilar = tk.BooleanVar(value=True)
        tk.Checkbutton(frame, text="Exclude Similar-looking Characters", variable=self.m_VarExcludeSimilar, font=label_font).grid(row=4, column=0, columnspan=2, pady=5)

        tk.Label(frame, text="Specific Characters to Include (leave blank if none):", font=label_font).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.m_EntryIncludeChars = tk.Entry(frame, font=label_font)
        self.m_EntryIncludeChars.grid(row=5, column=1, pady=5)

        tk.Label(frame, text="Specific Characters to Exclude (leave blank if none):", font=label_font).grid(row=6, column=0, sticky=tk.W, pady=5)
        self.m_EntryExcludeChars = tk.Entry(frame, font=label_font)
        self.m_EntryExcludeChars.grid(row=6, column=1, pady=5)

        generate_button = tk.Button(frame, text="Generate Passwords", command=self.GeneratePasswords, padx=10, pady=5, bg="#4CAF50", fg="white", font=button_font)
        generate_button.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Label(frame, text="Output:", font=("Cascadia Code", 12, "bold")).grid(row=8, column=0, columnspan=2, pady=5)

        self.m_TextArea = scrolledtext.ScrolledText(frame, width=70, height=20, font=("Cascadia Code", 10))
        self.m_TextArea.grid(row=9, column=0, columnspan=2, pady=10)

    def GeneratePasswords(self):
        try:
            length = int(self.m_EntryLength.get())
            count = int(self.m_EntryCount.get())
            include_special_chars = self.m_VarIncludeSpecial.get()
            exclude_similar_chars = self.m_VarExcludeSimilar.get()
            include_chars = self.m_EntryIncludeChars.get().strip()
            exclude_chars = self.m_EntryExcludeChars.get().strip()

            generator = SecurePasswordGenerator(
                length=length,
                exclude_similar_chars=exclude_similar_chars,
                include_chars=include_chars,
                exclude_chars=exclude_chars
            )
            passwords = generator.GenerateMultiplePasswords(count=count)
            self.m_TextArea.delete(1.0, tk.END)
            for pwd in passwords:
                self.m_TextArea.insert(tk.END, f"Generated Password: {pwd}\n")

            generator.SavePasswordsToFile(passwords)

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
