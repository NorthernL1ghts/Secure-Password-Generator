import tkinter as tk
from tkinter import messagebox, scrolledtext
from SecurePasswordGenerator import SecurePasswordGenerator

class Window:
    def __init__(self, root):
        self.m_Root = root
        self.m_Root.title("Secure Password Generator")
        self.m_Root.geometry("600x450")  # Set the window size to be wider

        self.CreateWidgets()

    def CreateWidgets(self):
        # Create and place widgets
        tk.Label(self.m_Root, text="Password Length (12-25):").grid(row=0, column=0, padx=10, pady=5)
        self.m_EntryLength = tk.Entry(self.m_Root)
        self.m_EntryLength.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.m_Root, text="Number of Passwords:").grid(row=1, column=0, padx=10, pady=5)
        self.m_EntryCount = tk.Entry(self.m_Root)
        self.m_EntryCount.grid(row=1, column=1, padx=10, pady=5)

        self.m_VarIncludeSpecial = tk.BooleanVar(value=True)
        tk.Checkbutton(self.m_Root, text="Include Special Characters", variable=self.m_VarIncludeSpecial).grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.m_VarExcludeSimilar = tk.BooleanVar(value=True)
        tk.Checkbutton(self.m_Root, text="Exclude Similar-looking Characters", variable=self.m_VarExcludeSimilar).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Label(self.m_Root, text="Specific Characters to Include (leave blank if none):").grid(row=4, column=0, padx=10, pady=5)
        self.m_EntryIncludeChars = tk.Entry(self.m_Root)
        self.m_EntryIncludeChars.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.m_Root, text="Specific Characters to Exclude (leave blank if none):").grid(row=5, column=0, padx=10, pady=5)
        self.m_EntryExcludeChars = tk.Entry(self.m_Root)
        self.m_EntryExcludeChars.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.m_Root, text="Generate Passwords", command=self.GeneratePasswords).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.m_TextArea = scrolledtext.ScrolledText(self.m_Root, width=60, height=20)
        self.m_TextArea.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

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

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
