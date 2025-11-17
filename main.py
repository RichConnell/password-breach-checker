###########################
# Password Breach Checker #
#     by Rich Connell     #
###########################
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox


# --------------------------
# THEME COLORS
# --------------------------
BG = "#0d0d0d"          # Main background
CARD_BG = "#1a1a1a"      # Card container
TEXT_COLOR = "#e6e6e6"
ACCENT = "#ff3b3b"
BTN_BG = "#b80000"
BTN_HOVER = "#d10000"
ENTRY_BG = "#262626"


def check_password_breach():
    password = entry.get()

    if not password:
        messagebox.showwarning("Input Required", "Please enter a password.")
        return

    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to retrieve breach information.")
        return

    found = False
    count = 0

    for line in response.text.splitlines():
        h_suffix, h_count = line.split(":")
        if h_suffix == suffix:
            found = True
            count = int(h_count)
            break

    if found:
        messagebox.showwarning(
            "⚠ Password Breached",
            f"⚠ This password was found in breaches {count:,} times.\n"
            "Do NOT use this password."
        )
    else:
        messagebox.showinfo(
            "✔ Safe Password",
            "✔ This password was NOT found in any known breaches."
        )

    entry.delete(0, tk.END)


# BUTTON HOVER EFFECTS
def on_hover(e):
    check_button.config(bg=BTN_HOVER)


def on_leave(e):
    check_button.config(bg=BTN_BG)


def on_enter_key(event):
    check_password_breach()


# --------------------------
# MAIN UI SETUP
# --------------------------
root = tk.Tk()
root.title("Password Breach Checker")
root.geometry("520x330")
root.configure(bg=BG)
root.resizable(False, False)

# Center the window
root.update_idletasks()
w = 520
h = 330
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

# --------------------------
# MAIN "CARD" CONTAINER
# --------------------------
card = tk.Frame(root, bg=CARD_BG, bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=260)

# Title
title = tk.Label(
    card,
    text="Password Breach Checker",
    font=("Segoe UI", 18, "bold"),
    fg=ACCENT,
    bg=CARD_BG
)
title.pack(pady=(15, 5))

# Subtitle
subtitle = tk.Label(
    card,
    text="Check if a password appears in known data breaches",
    font=("Segoe UI", 10),
    fg=TEXT_COLOR,
    bg=CARD_BG
)
subtitle.pack(pady=(0, 15))

# Password Entry
entry = tk.Entry(
    card,
    width=35,
    font=("Segoe UI", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    justify="center",
    show="•"
)
entry.pack(pady=10)

# Check Button
check_button = tk.Button(
    card,
    text="Check Password",
    command=check_password_breach,
    font=("Segoe UI Semibold", 12),
    fg="white",
    bg=BTN_BG,
    relief="flat",
    activebackground=BTN_HOVER,
    activeforeground="white",
    cursor="hand2",
    width=18,
    height=2
)
check_button.pack(pady=15)

# Hover effects
check_button.bind("<Enter>", on_hover)
check_button.bind("<Leave>", on_leave)

# Enter key triggers button
root.bind("<Return>", on_enter_key)

entry.focus()
root.mainloop()
