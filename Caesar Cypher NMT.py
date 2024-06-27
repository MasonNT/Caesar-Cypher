import tkinter as tk
from tkinter import ttk

def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A' ) + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a' ) + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def encrypt():
    plaintext = entry.get()
    shift = int(shift_entry.get())
    
    words = plaintext.split()
    encrypted_text = []

    for word in words:
        encrypted_word = caesar_cipher(word, shift)
        encrypted_text.append(encrypted_word)

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ' '.join(encrypted_text))
    result_text.config(state="disabled")

def decrypt():
    ciphertext = entry.get()
    shift = int(shift_entry.get())
    
    words = ciphertext.split()
    decrypted_text = []

    for word in words:
        decrypted_word = caesar_cipher(word, -shift)  
        decrypted_text.append(decrypted_word)

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ' '.join(decrypted_text))
    result_text.config(state="disabled")


window = tk.Tk()
window.title("Caesar Cipher Encryptor/Decryptor")


width = int(window.winfo_screenwidth() * 0.25)
height = int(window.winfo_screenheight() * 0.18)
window.geometry(f"{width}x{height}")


label = ttk.Label(window, text="Enter words separated by spaces:")
entry = ttk.Entry(window, width=70)  
shift_label = ttk.Label(window, text="Enter the shift value:")
shift_entry = ttk.Entry(window, width=10)
encrypt_button = ttk.Button(window, text="Encrypt", command=encrypt)
decrypt_button = ttk.Button(window, text="Decrypt", command=decrypt)


result_text = tk.Text(window, height=4, width=56, wrap=tk.WORD)
result_text.config(state="disabled")


label.grid(column=0, row=0, padx=10, pady=10, sticky="w")
entry.grid(column=1, row=0, columnspan=2, padx=10, pady=10, sticky="ew")  
shift_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")
shift_entry.grid(column=1, row=1, padx=10, pady=10)
encrypt_button.grid(column=0, row=2, pady=10)
decrypt_button.grid(column=1, row=2, pady=10)


result_text.grid(column=0, row=3, columnspan=2, pady=10, sticky="nsew")
window.grid_rowconfigure(3, weight=1)  
window.grid_columnconfigure(0, weight=1)  
window.grid_columnconfigure(1, weight=1)  


window.mainloop()
