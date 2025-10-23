import os
import tkinter as tk
import subprocess

root = tk.Tk()
root.title("File Organizer")

def open_dir(directory):
    #subprocess.Popen(["explorer", directory])  # Apre la cartella in Esplora file
    open_md(directory, 0)

def open_md(directory, index):
    reader = tk.Toplevel(root)
    reader.title(f"Reader - {os.path.basename(directory)}")
    md_files = [f for f in os.listdir(directory) if f.endswith(".md")]
    if md_files:
        with open(os.path.join(directory, md_files[index]), "r", encoding="UTF-8") as f:
            content = f.read()
        text_box = tk.Text(reader, wrap="word", width=80, height=25)
        text_box.insert("1.0", content)
        text_box.config(state="disabled")  # Rende il testo non modificabile
        text_box.pack(expand=True, fill="both")

        scrollbar = tk.Scrollbar(reader, command=text_box.yview)
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tk.Button(reader, text="Close", command=reader.destroy).pack(pady=5)
        tk.Button(reader, text="next",state="normal" if index <= len(md_files) else "disabled",  command=lambda: (reader.destroy(),open_md(directory, index+1))).pack(pady=5)
        tk.Button(reader, text="previous",state="normal" if index >0  else "disabled", command=lambda: (reader.destroy(), open_md(directory, index-1))).pack(pady=5)
    else:
        print("Nessun file markdown trovato nella cartella.")

#Crea un nuovo argomento  nella cartella selezionata
def new_dir(directory, name):
    os.makedirs(f"./{directory}/{name}")
    clear_name = ''.join([c for c in name if not c.isdigit()]).strip().capitalize() # Rimuove i numeri e formatta il nome
    f = open(f"./{directory}/{name}/00 {clear_name}.md", "w")
    f.write(f"# 00 {clear_name}\n - \n ## Riferimenti \n - ")
    f.close()



files = os.listdir("./")
buttons = []
j_buttons = []
input_boxes = []
new_button = []

col = 0

for folder in files:
    # esclude file e cartelle non desiderate
    if folder in [".obsidian", "Organizer.py", "Templates", "Canvas", "Source", "Template", "Organizer.exe"] or not os.path.isdir(f"./{folder}"):
        continue

    # crea il bottone per la cartella
    btn = tk.Button(root, text=f"📂 |          {folder}           | ")
    btn.grid(column=col, row=0, padx=10, pady=10)
    buttons.append(btn)

    # mostra i file interni
    j_files = os.listdir(f"./{folder}")
    for row, j_file in enumerate(j_files, start=1):
        new_entry = tk.Entry(root)
        new_entry.grid(column=col, row=len(j_files)+2)
        input_boxes.append(new_entry)
        j_btn = tk.Button(root, text=f"📂  |-> {j_file} | ", command=lambda f=folder, j=j_file: open_dir(os.path.abspath(f"./{f}/{j}")), borderwidth=1, relief="solid", padx=10, pady=2).grid(column=col, row=row, sticky="nsew")
        j_buttons.append(j_btn)
        new_btn = tk.Button(root, text="📂 New", borderwidth=1, relief="solid", padx=10, pady=2, command=lambda f=folder, n= 
                            new_entry: new_dir(f,n.get())).grid(column=col,row=len(j_files)+1)
        new_button.append(new_btn)

    #print(os.listdir(f"./{folder}/{j_files[0]}"))
    col += 1


root.mainloop()
