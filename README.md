# Cipher Toolkit

A Python desktop application for exploring, encrypting, and decrypting classical ciphers through an interactive GUI.

This project was built as an educational cryptography tool to demonstrate how historic cipher systems work, how their keys affect output, and why many of these methods are no longer secure by modern standards. It is designed for learning, experimentation, and classroom-style demonstration rather than real-world secure communication.
How to Run
Make sure Python 3 is installed
Clone the repository
Run the application
python CipherToolkit.py
How to Use
Launch the application
Select a cipher from the available options
Enter the text you want to process
Enter the required key if the cipher needs one
Choose whether to encrypt or decrypt
Copy the output for further use or comparison
Example Learning Goals

This project can be used to:

compare substitution and transposition ciphers
see how keys change encryption output
understand why simple classical ciphers are vulnerable
demonstrate historical cryptography concepts in a visual format
Notes

This project is for educational use only. The ciphers included here are not secure for modern communication and should not be used to protect sensitive information.
Potential improvements include:

adding frequency analysis tools
adding brute-force demonstrations for weaker ciphers
exporting results to text files
improving validation and error messaging
packaging the application as a standalone executable
Author

Nikoles Tobin

Electrical Engineering student interested in automation, systems, and technical problem-solving.



## Features

- GUI-based desktop application built with Python and Tkinter
- Encrypt and decrypt text using multiple classical ciphers
- Supports both single-word and paragraph-length input
- Dynamic key input based on the selected cipher
- Built-in historical background for each cipher
- Educational focus on how cipher logic and keying methods work

## Supported Ciphers

- Caesar Cipher
- ROT13
- Atbash Cipher
- Vigenère Cipher
- Rail Fence Cipher
- Columnar Transposition
- Affine Cipher
- Simple Substitution
- Morse Code

## Why I Built This

I built this project to strengthen my understanding of:
- string manipulation in Python
- algorithm design and modular logic
- GUI development with Tkinter
- input handling and user interaction
- how classical encryption methods evolved over time

It also served as a way to turn abstract cryptography concepts into something interactive and easier to demonstrate.

## Tech Stack

- Python
- Tkinter

## Project Structure




```text
Teaching_Cipher-Toolkit/
├── CipherToolkit.py
└── README.md
