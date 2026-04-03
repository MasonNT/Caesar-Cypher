import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
import random
import math

# ─── Theme colours ───────────────────────────────────────────────────────────
BG           = "#1e1e2e"
BG_SECONDARY = "#282840"
BG_CARD      = "#313150"
FG           = "#cdd6f4"
FG_DIM       = "#8888aa"
ACCENT       = "#89b4fa"
ACCENT_HOVER = "#b4d8fd"
GREEN        = "#a6e3a1"
RED          = "#f38ba8"
ORANGE       = "#fab387"
BORDER       = "#45456a"
ENTRY_BG     = "#3b3b5c"

# ─── Cipher implementations ─────────────────────────────────────────────────

def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def rot13_cipher(text, _shift=None, decrypt=False):
    return caesar_cipher(text, 13)


def atbash_cipher(text, _shift=None, decrypt=False):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr(base + 25 - (ord(ch) - base)))
        else:
            result.append(ch)
    return ''.join(result)


def vigenere_cipher(text, key, decrypt=False):
    if not key or not key.isalpha():
        return "[Error: Vigenère key must be alphabetic]"
    key = key.upper()
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            k = ord(key[ki % len(key)]) - ord('A')
            if decrypt:
                k = -k
            result.append(chr((ord(ch) - base + k) % 26 + base))
            ki += 1
        else:
            result.append(ch)
    return ''.join(result)


def rail_fence_cipher(text, rails, decrypt=False):
    try:
        rails = int(rails) if not isinstance(rails, int) else rails
    except (ValueError, TypeError):
        return "[Error: Rails must be a number]"
    if rails < 2:
        return "[Error: Need at least 2 rails]"
    if not decrypt:
        fence = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for ch in text:
            fence[rail].append(ch)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return ''.join(''.join(r) for r in fence)
    else:
        pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
        indices = [[] for _ in range(rails)]
        for i in range(len(text)):
            indices[pattern[i % len(pattern)]].append(i)
        result = [''] * len(text)
        pos = 0
        for rail in range(rails):
            for idx in indices[rail]:
                if pos < len(text):
                    result[idx] = text[pos]
                    pos += 1
        return ''.join(result)


def columnar_transposition(text, key, decrypt=False):
    if not key:
        return "[Error: Key required]"
    key = key.upper()
    n_cols = len(key)
    order = sorted(range(n_cols), key=lambda i: key[i])

    if not decrypt:
        padding = (n_cols - len(text) % n_cols) % n_cols
        text += 'X' * padding
        n_rows = len(text) // n_cols
        grid = [text[i * n_cols:(i + 1) * n_cols] for i in range(n_rows)]
        return ''.join(''.join(grid[r][c] for r in range(n_rows)) for c in order)
    else:
        n_rows = math.ceil(len(text) / n_cols)
        total = n_rows * n_cols
        padding = total - len(text)
        col_lengths = [n_rows] * n_cols
        inv_order = sorted(range(n_cols), key=lambda i: order[i])
        for i in range(padding):
            col_lengths[inv_order[-(i + 1)]] -= 1
        cols = {}
        pos = 0
        for c in order:
            cols[c] = text[pos:pos + col_lengths[c]]
            pos += col_lengths[c]
        result = []
        for r in range(n_rows):
            for c in range(n_cols):
                if r < len(cols[c]):
                    result.append(cols[c][r])
        return ''.join(result).rstrip('X')


def affine_cipher(text, key, decrypt=False):
    try:
        parts = str(key).split(',')
        a, b = int(parts[0].strip()), int(parts[1].strip())
    except (ValueError, IndexError):
        return "[Error: Key must be 'a, b' e.g. '5, 8']"
    if math.gcd(a, 26) != 1:
        return f"[Error: 'a' ({a}) must be coprime with 26]"

    if not decrypt:
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((a * (ord(ch) - base) + b) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)
    else:
        a_inv = pow(a, -1, 26)
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((a_inv * ((ord(ch) - base) - b)) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)


def substitution_cipher(text, key, decrypt=False):
    if not key or len(key) != 26 or not key.isalpha():
        alpha = list(string.ascii_uppercase)
        random.seed(key if key else 42)
        shuffled = alpha[:]
        random.shuffle(shuffled)
        key = ''.join(shuffled)
    key = key.upper()
    if not decrypt:
        table_upper = str.maketrans(string.ascii_uppercase, key)
        table_lower = str.maketrans(string.ascii_lowercase, key.lower())
    else:
        table_upper = str.maketrans(key, string.ascii_uppercase)
        table_lower = str.maketrans(key.lower(), string.ascii_lowercase)
    return text.translate(table_upper).translate(table_lower)


def morse_code_cipher(text, _key=None, decrypt=False):
    MORSE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.', ' ': '/',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
    }
    if not decrypt:
        result = []
        for ch in text.upper():
            result.append(MORSE.get(ch, ch))
        return ' '.join(result)
    else:
        REVERSE = {v: k for k, v in MORSE.items()}
        parts = text.strip().split(' ')
        result = []
        for p in parts:
            result.append(REVERSE.get(p, p))
        return ''.join(result)


# ─── Cipher metadata ────────────────────────────────────────────────────────

CIPHERS = {
    "Caesar Cipher": {
        "func": caesar_cipher,
        "key_label": "Shift (1-25):",
        "key_hint": "e.g. 3",
        "needs_key": True,
        "history": (
            "One of the oldest known ciphers, used by Julius Caesar around 58 BC to "
            "protect military correspondence during the Gallic Wars. Each letter is "
            "shifted by a fixed number of positions in the alphabet.\n\n"
            "STATUS: Educational use only — trivially breakable with just 25 attempts. "
            "Still taught as an introduction to cryptography in schools worldwide."
        ),
    },
    "ROT13": {
        "func": rot13_cipher,
        "key_label": "(No key needed)",
        "key_hint": "",
        "needs_key": False,
        "history": (
            "A special case of the Caesar cipher with a fixed shift of 13. Because the "
            "alphabet has 26 letters, applying ROT13 twice returns the original text.\n\n"
            "STATUS: Still actively used on internet forums and Usenet to hide spoilers, "
            "puzzle answers, and mildly sensitive content. Built into many Unix systems "
            "as a standard utility."
        ),
    },
    "Atbash Cipher": {
        "func": atbash_cipher,
        "key_label": "(No key needed)",
        "key_hint": "",
        "needs_key": False,
        "history": (
            "Originally a Hebrew cipher from approximately 500 BC, Atbash maps each "
            "letter to its reverse in the alphabet (A↔Z, B↔Y, etc.). It appears in "
            "the Bible — the word 'Sheshach' in the Book of Jeremiah is believed to be "
            "an Atbash encoding of 'Babel' (Babylon).\n\n"
            "STATUS: Obsolete for security. Used as a teaching tool and in puzzle games."
        ),
    },
    "Vigenère Cipher": {
        "func": vigenere_cipher,
        "key_label": "Keyword:",
        "key_hint": "e.g. LEMON",
        "needs_key": True,
        "history": (
            "Described by Giovan Battista Bellaso in 1553 and later misattributed to "
            "Blaise de Vigenère, this polyalphabetic cipher was considered unbreakable "
            "for over 300 years — earning the nickname 'le chiffre indéchiffrable'. "
            "It was broken by Charles Babbage and Friedrich Kasiski in the 1860s.\n\n"
            "STATUS: No longer secure, but foundational to modern cryptography. Its "
            "concepts underpin more advanced ciphers used today."
        ),
    },
    "Rail Fence Cipher": {
        "func": rail_fence_cipher,
        "key_label": "Number of rails:",
        "key_hint": "e.g. 3",
        "needs_key": True,
        "history": (
            "A transposition cipher used during the American Civil War, the Rail Fence "
            "writes plaintext in a zigzag pattern across a number of 'rails', then reads "
            "off each row to produce ciphertext. It rearranges letter positions rather "
            "than substituting letters.\n\n"
            "STATUS: Too simple for real security. Commonly used in CTF (Capture the Flag) "
            "competitions and cryptography education."
        ),
    },
    "Columnar Transposition": {
        "func": columnar_transposition,
        "key_label": "Keyword:",
        "key_hint": "e.g. ZEBRA",
        "needs_key": True,
        "history": (
            "Widely used during World War I and World War II, this cipher writes the "
            "message into a grid row-by-row, then reads columns in an order determined "
            "by alphabetically sorting a keyword. The German ADFGVX cipher combined "
            "it with a Polybius square for added security.\n\n"
            "STATUS: Obsolete alone, but double transposition remained in military use "
            "into the mid-20th century. The concept of permutation-based encryption "
            "persists in modern block ciphers."
        ),
    },
    "Affine Cipher": {
        "func": affine_cipher,
        "key_label": "Key (a, b):",
        "key_hint": "e.g. 5, 8",
        "needs_key": True,
        "history": (
            "A mathematical cipher that encrypts each letter using the formula "
            "E(x) = (ax + b) mod 26, where 'a' must be coprime with 26. It generalises "
            "both the Caesar cipher (a=1) and the multiplicative cipher (b=0).\n\n"
            "STATUS: Educational and academic use. Commonly appears in university "
            "cryptography and number theory courses to illustrate modular arithmetic "
            "and the concept of key spaces."
        ),
    },
    "Simple Substitution": {
        "func": substitution_cipher,
        "key_label": "Seed word or 26-letter key:",
        "key_hint": "e.g. SECRET or QWERTYUIOPASDFGHJKLZXCVBNM",
        "needs_key": True,
        "history": (
            "The general monoalphabetic substitution cipher has been used since at least "
            "the 9th century. Al-Kindi, the Arab polymath, wrote the first known treatise "
            "on cryptanalysis (frequency analysis) to break it around 850 AD. With 26! "
            "(≈ 4 × 10²⁶) possible keys, brute force is impractical — but frequency "
            "analysis defeats it easily.\n\n"
            "STATUS: Not secure. Famously featured in Edgar Allan Poe's 'The Gold-Bug' "
            "and Arthur Conan Doyle's 'The Adventure of the Dancing Men'. Popular in "
            "newspaper cryptogram puzzles."
        ),
    },
    "Morse Code": {
        "func": morse_code_cipher,
        "key_label": "(No key needed)",
        "key_hint": "",
        "needs_key": False,
        "history": (
            "Developed by Samuel Morse and Alfred Vail in the 1830s–1840s for use with "
            "the electric telegraph. Morse Code is technically an encoding rather than "
            "a cipher — it was designed for communication, not secrecy.\n\n"
            "STATUS: Still actively used! Required for amateur (ham) radio licences in "
            "many countries. Used in aviation and maritime as a backup system, and the "
            "SOS distress signal (··· ——— ···) remains universally recognised."
        ),
    },
}


# ─── GUI Application ────────────────────────────────────────────────────────

class CipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cipher Toolkit — Encrypt · Decrypt · Learn")
        self.configure(bg=BG)
        self.minsize(960, 720)

        # Centre on screen
        w, h = 1020, 760
        sx = self.winfo_screenwidth() // 2 - w // 2
        sy = self.winfo_screenheight() // 2 - h // 2
        self.geometry(f"{w}x{h}+{sx}+{sy}")

        self._build_styles()
        self._build_ui()

    # ── ttk styles ──────────────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=BG, foreground=FG, font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=BG_CARD)
        style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        style.configure("Card.TLabel", background=BG_CARD, foreground=FG)
        style.configure("Dim.TLabel", background=BG, foreground=FG_DIM, font=("Segoe UI", 9))
        style.configure("CardDim.TLabel", background=BG_CARD, foreground=FG_DIM, font=("Segoe UI", 9))
        style.configure("Header.TLabel", background=BG, foreground=ACCENT,
                        font=("Segoe UI Semibold", 18))
        style.configure("SubHeader.TLabel", background=BG_CARD, foreground=ACCENT,
                        font=("Segoe UI Semibold", 11))
        style.configure("CipherName.TLabel", background=BG_CARD, foreground=FG,
                        font=("Segoe UI Semibold", 10))

        # Buttons
        style.configure("Accent.TButton", background=ACCENT, foreground=BG,
                        font=("Segoe UI Semibold", 10), padding=(18, 8))
        style.map("Accent.TButton",
                  background=[("active", ACCENT_HOVER), ("pressed", ACCENT_HOVER)])

        style.configure("Green.TButton", background=GREEN, foreground=BG,
                        font=("Segoe UI Semibold", 10), padding=(18, 8))
        style.map("Green.TButton",
                  background=[("active", "#c6f6c1"), ("pressed", "#c6f6c1")])

        style.configure("Red.TButton", background=RED, foreground=BG,
                        font=("Segoe UI Semibold", 10), padding=(18, 8))
        style.map("Red.TButton",
                  background=[("active", "#f9b4c4"), ("pressed", "#f9b4c4")])

        # Combobox
        style.configure("TCombobox", fieldbackground=ENTRY_BG, foreground=FG,
                        selectbackground=ACCENT, selectforeground=BG,
                        padding=6)
        style.map("TCombobox", fieldbackground=[("readonly", ENTRY_BG)])

        # Radiobutton used for cipher list
        style.configure("Cipher.TRadiobutton", background=BG_CARD, foreground=FG,
                        font=("Segoe UI", 10), padding=(8, 6))
        style.map("Cipher.TRadiobutton",
                  background=[("active", BG_SECONDARY)],
                  foreground=[("selected", ACCENT)])

    # ── main layout ─────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = ttk.Frame(self)
        hdr.pack(fill="x", padx=20, pady=(16, 4))
        ttk.Label(hdr, text="⬡  Cipher Toolkit", style="Header.TLabel").pack(side="left")
        ttk.Label(hdr, text="Explore classical ciphers — encrypt, decrypt & learn their history",
                  style="Dim.TLabel").pack(side="left", padx=(14, 0), pady=(6, 0))

        sep = tk.Frame(self, bg=BORDER, height=1)
        sep.pack(fill="x", padx=20, pady=(8, 12))

        # Body: left panel (cipher list) + right panel (workspace)
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_left_panel(body)
        self._build_right_panel(body)

        # Select first cipher
        self.selected_cipher.set(list(CIPHERS.keys())[0])
        self._on_cipher_change()

    # ── left: cipher selector ───────────────────────────────────────────
    def _build_left_panel(self, parent):
        left = ttk.Frame(parent, style="Card.TFrame", width=220)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        left.grid_propagate(False)
        left.configure(width=230)

        ttk.Label(left, text="CIPHERS", style="SubHeader.TLabel").pack(
            anchor="w", padx=14, pady=(14, 6))

        self.selected_cipher = tk.StringVar()
        for name in CIPHERS:
            rb = ttk.Radiobutton(left, text=name, variable=self.selected_cipher,
                                 value=name, style="Cipher.TRadiobutton",
                                 command=self._on_cipher_change)
            rb.pack(fill="x", padx=6, pady=1)

    # ── right: workspace ────────────────────────────────────────────────
    def _build_right_panel(self, parent):
        right = ttk.Frame(parent)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        # Row 0 — history card
        history_card = ttk.Frame(right, style="Card.TFrame")
        history_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.history_title = ttk.Label(history_card, text="", style="SubHeader.TLabel")
        self.history_title.pack(anchor="w", padx=14, pady=(12, 4))

        self.history_text = tk.Text(history_card, wrap="word", height=6, bd=0,
                                     bg=BG_CARD, fg=FG_DIM, font=("Segoe UI", 9),
                                     highlightthickness=0, padx=14, pady=4,
                                     cursor="arrow", state="disabled")
        self.history_text.pack(fill="x", padx=(0, 8), pady=(0, 10))

        # Row 1 — input area
        input_frame = ttk.Frame(right, style="Card.TFrame")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Input Text:", style="Card.TLabel").grid(
            row=0, column=0, padx=(14, 6), pady=(12, 6), sticky="nw")
        self.input_text = tk.Text(input_frame, wrap="word", height=4, bd=0,
                                   bg=ENTRY_BG, fg=FG, font=("Consolas", 10),
                                   insertbackground=ACCENT, highlightthickness=1,
                                   highlightcolor=ACCENT, highlightbackground=BORDER,
                                   padx=8, pady=6)
        self.input_text.grid(row=0, column=1, padx=(0, 14), pady=(12, 6), sticky="ew")

        # Key row
        self.key_label = ttk.Label(input_frame, text="Key:", style="Card.TLabel")
        self.key_label.grid(row=1, column=0, padx=(14, 6), pady=(0, 12), sticky="w")

        key_wrapper = ttk.Frame(input_frame, style="Card.TFrame")
        key_wrapper.grid(row=1, column=1, padx=(0, 14), pady=(0, 12), sticky="ew")
        key_wrapper.columnconfigure(0, weight=0)

        self.key_entry = tk.Entry(key_wrapper, bg=ENTRY_BG, fg=FG,
                                   font=("Consolas", 10), insertbackground=ACCENT,
                                   highlightthickness=1, highlightcolor=ACCENT,
                                   highlightbackground=BORDER, bd=0, width=28)
        self.key_entry.pack(side="left", ipady=4)

        self.key_hint = ttk.Label(key_wrapper, text="", style="CardDim.TLabel")
        self.key_hint.pack(side="left", padx=(10, 0))

        # Buttons
        btn_frame = ttk.Frame(input_frame, style="Card.TFrame")
        btn_frame.grid(row=2, column=0, columnspan=2, padx=14, pady=(0, 14), sticky="w")

        ttk.Button(btn_frame, text="🔒  Encrypt", style="Green.TButton",
                   command=self._encrypt).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="🔓  Decrypt", style="Red.TButton",
                   command=self._decrypt).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="⟲  Clear", style="Accent.TButton",
                   command=self._clear).pack(side="left")

        # Row 2 — output area
        output_card = ttk.Frame(right, style="Card.TFrame")
        output_card.grid(row=2, column=0, sticky="nsew", pady=(0, 0))
        right.rowconfigure(2, weight=1)

        ttk.Label(output_card, text="OUTPUT", style="SubHeader.TLabel").pack(
            anchor="w", padx=14, pady=(12, 4))

        self.output_text = tk.Text(output_card, wrap="word", height=6, bd=0,
                                    bg=BG_SECONDARY, fg=GREEN, font=("Consolas", 11),
                                    highlightthickness=0, padx=14, pady=8,
                                    cursor="arrow", state="disabled")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 12))

    # ── event handlers ──────────────────────────────────────────────────
    def _on_cipher_change(self, *_):
        name = self.selected_cipher.get()
        info = CIPHERS[name]

        # Update history
        self.history_title.configure(text=f"History — {name}")
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.insert("1.0", info["history"])
        self.history_text.configure(state="disabled")

        # Update key field
        self.key_label.configure(text=info["key_label"])
        self.key_hint.configure(text=info["key_hint"])
        if info["needs_key"]:
            self.key_entry.configure(state="normal")
            self.key_entry.delete(0, "end")
        else:
            self.key_entry.delete(0, "end")
            self.key_entry.configure(state="disabled")

    def _get_inputs(self):
        name = self.selected_cipher.get()
        info = CIPHERS[name]
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get().strip()
        if not text.strip():
            messagebox.showwarning("Input needed", "Please enter some text to process.")
            return None
        return name, info, text, key

    def _show_output(self, result):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")

    def _encrypt(self):
        inputs = self._get_inputs()
        if not inputs:
            return
        name, info, text, key = inputs
        func = info["func"]
        if info["needs_key"]:
            result = func(text, key if not key.isdigit() else int(key), decrypt=False)
        else:
            result = func(text, decrypt=False)
        self._show_output(result)

    def _decrypt(self):
        inputs = self._get_inputs()
        if not inputs:
            return
        name, info, text, key = inputs
        func = info["func"]
        if info["needs_key"]:
            result = func(text, key if not key.isdigit() else int(key), decrypt=True)
        else:
            result = func(text, decrypt=True)
        self._show_output(result)

    def _clear(self):
        self.input_text.delete("1.0", "end")
        self.key_entry.configure(state="normal")
        self.key_entry.delete(0, "end")
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self._on_cipher_change()


if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()
