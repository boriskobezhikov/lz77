import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher


def encode(search_size, lookahead_size, input_text):
    i = 0
    search_buffer = ''
    lookahead_buffer = input_text[:lookahead_size]
    encoded_data = []
    while lookahead_buffer:
        seqMatch = SequenceMatcher(None, search_buffer, lookahead_buffer)
        offset = 0
        length = 0
        char = ''
        matches = seqMatch.get_matching_blocks()
        for j in range(len(search_buffer)):
            if search_buffer[j] == lookahead_buffer[0]:
                offset = len(search_buffer) - j
                length = 1
                char_pos = min(len(input_text) - 1, i + length)
                char = input_text[char_pos]
        for match in matches:
            if match.b == 0 and match.size > length:
                offset = len(search_buffer) - match.a
                length = match.size
                char_pos = min(len(input_text) - 1, i + length)
                char = input_text[char_pos]
        if offset == 0 and length == 0:
            encoded_data.append((0, 0, input_text[i]))
            i += 1
        else:
            encoded_data.append((offset, length, char))
            i += length + 1
        la = min(len(input_text), i + lookahead_size)
        s = max(0, i - search_size)
        lookahead_buffer = input_text[i:la]
        search_buffer = input_text[s:i]
    
    return encoded_data


def decode(encoded_data):
    decoded_text = ''
    for entry in encoded_data:
        offset, length, char = entry
        if offset == 0 and length == 0:
            decoded_text += char
        else:
            search_start = len(decoded_text) - offset
            search_end = search_start + length
            search_buffer = decoded_text[search_start:search_end]
            decoded_text += search_buffer + char
    
    return decoded_text


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return None


def save_file(content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


def submit_form():
    search_size = int(search_size_entry.get())
    lookahead_size = int(lookahead_size_entry.get())
    file_content = open_file()
    if file_content:
        if encode_flag.get() == 1:
            encoded_data = encode(search_size, lookahead_size, file_content)
            encoded_text = '\n'.join([f"{offset} {length} {char}" for offset, length, char in encoded_data])
            save_file(encoded_text)
        else:
            decoded_data = []
            for line in file_content.split('\n'):
                offset, length, char = line.split()
                decoded_data.append((int(offset), int(length), char))
            decoded_text = decode(decoded_data)
            save_file(decoded_text)
        status_label.config(text="Operation completed successfully.")
    else:
        status_label.config(text="No file selected.")


window = tk.Tk()
window.title("LZ77")

tk.Label(window, text="Размер буфера поиска:").grid(row=0, column=0, padx=10, pady=10)
search_size_entry = tk.Entry(window)
search_size_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Label(window, text="Размер буфера кодирования:").grid(row=1, column=0, padx=10, pady=10)
lookahead_size_entry = tk.Entry(window)
lookahead_size_entry.grid(row=1, column=1, padx=10, pady=10)

encode_flag = tk.IntVar()
encode_flag.set(1)
encode_radio = tk.Radiobutton(window, text="Сжать", variable=encode_flag, value=1)
decode_radio = tk.Radiobutton(window, text="Расшифровать", variable=encode_flag, value=0)
encode_radio.grid(row=3, column=0, padx=10, pady=5)
decode_radio.grid(row=3, column=1, padx=10, pady=5)

submit_button = tk.Button(window, text="GO", command=submit_form)
submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

status_label = tk.Label(window, text="")
status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

window.mainloop()
