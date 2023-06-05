from difflib import SequenceMatcher


def encode(search_size, lookahead_size):
    with open("test.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    i = 0
    search_buffer = ''
    lookahead_buffer = input_text[:lookahead_size]
    with open("encode.txt", "w", encoding="utf-8") as f:
        while lookahead_buffer:
            seqMatch = SequenceMatcher(None, search_buffer, lookahead_buffer)
            offset = 0
            length = 0
            char = ''
            matches = seqMatch.get_matching_blocks()
            for j in range(len(search_buffer)):
                if (search_buffer[j] == lookahead_buffer[0]):
                    offset = len(search_buffer) - j
                    length = 1
                    char_pos = min(len(input_text) - 1, i+length)
                    char = input_text[char_pos]
            for match in matches:
                if match.b == 0 and match.size > length:
                    offset = len(search_buffer) - match.a
                    length = match.size
                    char_pos = min(len(input_text) - 1, i+length)
                    char = input_text[char_pos]
            if offset == 0 and length == 0:
                f.write(f"{0} {0} {input_text[i]}\n")
                print(f"{0} {0} {input_text[i]}\n")
                i += 1
            else:
                f.write(f"{offset} {length} {char}\n")
                print(f"{offset} {length} {char}\n")
                i += length + 1
            la = min(len(input_text), i + lookahead_size)
            s = max(0, i - search_size)
            lookahead_buffer = input_text[i:la]
            search_buffer = input_text[s:i]


def decode():
    encoded_data = []
    with open("encode.txt", "r", encoding="utf-8") as f:
        for line in f:
            offset, length, char = line.split()
            offset = int(offset)
            length = int(length)
            encoded_data.append((offset, length, char))

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

    with open("decode.txt", "w", encoding="utf-8") as file:
        file.write(decoded_text)


encode(30, 5)
decode()
