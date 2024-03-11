


def get_start_of_message_index(buffer: str, marker_length: int = 4):

    if len(buffer) < marker_length:
        raise ValueError("Buffer's length is lower than the start marker's")

    for index in range(marker_length, len(buffer)):
        chunk = buffer[index-marker_length:index]
        if len(set(chunk)) == marker_length:
            return index

    raise ValueError("Start marker not found in buffer!")

def main():
    with open(INPUT_FILE_PATH, encoding='utf-8') as input_file:
        buffer = input_file.read().strip()

    starting_index = get_start_of_message_index(buffer)
    print(f'Starting index {starting_index} (marker of 4 characters)')

    starting_index = get_start_of_message_index(buffer, 14)
    print(f'Starting index {starting_index} (marker of 14 characters)')


if __name__ == "__main__":
    INPUT_FILE_PATH = 'input.txt'
    main()
