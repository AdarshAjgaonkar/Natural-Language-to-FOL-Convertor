import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from infer_transformer import predict, format_predicates, logical_reasoning
import infer_transformer
print("FILE BEING USED:", infer_transformer.__file__)
# ---------------- ROOT ----------------
root = tk.Tk()
root.title("FOL Converter AI")
root.state("zoomed")  # fullscreen
root.configure(bg="#0b0f1a")

# ---------------- FADE IN ----------------
def fade_in(alpha=0):
    alpha += 0.04
    if alpha <= 1:
        root.attributes("-alpha", alpha)
        root.after(20, fade_in, alpha)

root.attributes("-alpha", 0)
fade_in()

# ---------------- BACKGROUND BLUR ----------------
bg = Image.new("RGB", (1200, 800), "#0b0f1a")

for color, pos in [
    ("#1e3a8a", (50, 50, 400, 400)),
    ("#9333ea", (600, 200, 1100, 700)),
    ("#0ea5e9", (300, 500, 800, 900))
]:
    overlay = Image.new("RGB", (1200, 800), "#0b0f1a")
    overlay.paste(color, pos)
    bg = Image.blend(bg, overlay, 0.3)

bg = bg.filter(ImageFilter.GaussianBlur(50))
bg_img = ImageTk.PhotoImage(bg)

bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1, relheight=1)

# ---------------- MAIN CONTAINER ----------------
main = tk.Frame(root, bg="#0b0f1a")
main.pack(fill="both", expand=True)

main.grid_rowconfigure(2, weight=1)
main.grid_columnconfigure(0, weight=1)

# ---------------- HEADER ----------------
tk.Label(main,
         text="Natural Language → FOL",
         font=("Segoe UI", 24, "bold"),
         fg="white",
         bg="#0b0f1a").grid(row=0, column=0, pady=(20, 5))

tk.Label(main,
         text="AI-powered logic + reasoning",
         font=("Segoe UI", 11),
         fg="#94a3b8",
         bg="#0b0f1a").grid(row=1, column=0)

# ---------------- INPUT CARD ----------------
input_card = tk.Frame(main, bg="#111827")
input_card.grid(row=2, column=0, padx=80, pady=20, sticky="ew")

# Sentence input
entry = tk.Entry(input_card,
                 font=("Segoe UI", 13),
                 bg="#020617",
                 fg="white",
                 insertbackground="white",
                 bd=0)
entry.pack(fill="x", padx=20, pady=(15, 5))

# Question input
question_entry = tk.Entry(input_card,
                         font=("Segoe UI", 11),
                         bg="#020617",
                         fg="#9ca3af",
                         insertbackground="white",
                         bd=0)
question_entry.pack(fill="x", padx=20, pady=(0, 10))
question_entry.insert(0, "Optional: Ask a question...")

# ---------------- SPINNER ----------------
spinner_label = tk.Label(input_card, text="", fg="white", bg="#111827", font=("Segoe UI", 12))
spinner_label.pack()

spinner_running = False
spinner_states = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def start_spinner(i=0):
    if spinner_running:
        spinner_label.config(text=spinner_states[i % len(spinner_states)])
        root.after(80, start_spinner, i + 1)

def stop_spinner():
    spinner_label.config(text="")

# ---------------- OUTPUT CARD ----------------
output_frame = tk.Frame(main, bg="#111827")
output_frame.grid(row=3, column=0, padx=80, pady=10, sticky="nsew")

output_box = tk.Text(output_frame,
                     font=("Consolas", 11),
                     bg="#020617",
                     fg="#e2e8f0",
                     insertbackground="white",
                     bd=0,
                     padx=20,
                     pady=20)

output_box.pack(fill="both", expand=True)
output_box.config(state="disabled")

# ---------------- FLOATING COPY BUTTON ----------------
def copy_output():
    text = output_box.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)

    copy_btn.config(text="✔")
    root.after(1000, lambda: copy_btn.config(text="⧉"))

copy_btn = tk.Label(output_frame,
                    text="⧉",
                    font=("Segoe UI", 11, "bold"),
                    fg="#9ca3af",
                    bg="#020617",
                    cursor="hand2")

copy_btn.place(relx=0.98, rely=0.02, anchor="ne")

copy_btn.bind("<Button-1>", lambda e: copy_output())
copy_btn.bind("<Enter>", lambda e: copy_btn.config(fg="white"))
copy_btn.bind("<Leave>", lambda e: copy_btn.config(fg="#9ca3af"))

# ---------------- TYPEWRITER ----------------
def typewriter(text):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)

    def animate(i=0):
        if i <= len(text):
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, text[:i])
            root.after(2, animate, i + 1)
        else:
            output_box.config(state="disabled")

    animate()

# ---------------- MAIN LOGIC ----------------
def run_model():
    global spinner_running

    sentence = entry.get().strip()

    if not sentence:
        typewriter("⚠ Please enter a sentence.")
        return

    spinner_running = True
    start_spinner()

    root.after(300, lambda: generate(sentence))

def generate(sentence):
    global spinner_running

    fol = predict(sentence)
    preds = format_predicates(fol)

    question = question_entry.get().strip()
    answer = ""

    if question and "Optional" not in question:
        answer = logical_reasoning(fol, question)

    result = "◆ Predicates\n\n"
    for i, (name, args, desc) in enumerate(preds, 1):
        result += f"{i}. {name}({', '.join(args)})\n   → {desc}.\n\n"

    result += "\n◆ FOL Representation\n\n" + fol

    if answer:
        result += "\n\n◆ Answer\n\n" + answer

    spinner_running = False
    stop_spinner()

    typewriter(result)

# ---------------- BUTTON ----------------
btn = tk.Button(input_card,
                text="Convert",
                command=run_model,
                font=("Segoe UI", 11, "bold"),
                fg="white",
                bg="#2563eb",
                activebackground="#1d4ed8",
                bd=0,
                padx=20,
                pady=10,
                cursor="hand2")

btn.pack(pady=10)

btn.bind("<Enter>", lambda e: btn.config(bg="#3b82f6"))
btn.bind("<Leave>", lambda e: btn.config(bg="#2563eb"))

entry.bind("<Return>", lambda e: run_model())

# ---------------- RUN ----------------
root.mainloop()