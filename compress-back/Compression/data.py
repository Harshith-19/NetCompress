import os
import json


def compress_lz77(data):
    compressed_data = []
    window_size = 12
    lookahead_buffer_size = 5
    pos = 0

    while pos < len(data):
        match_found = False
        match_length = 0
        match_distance = 0

        window_start = max(0, pos - window_size)
        search_window = data[window_start:pos]
        lookahead_buffer = data[pos:pos + lookahead_buffer_size]

        for i in range(len(search_window)):
            j = 0
            while j < len(lookahead_buffer) and search_window[i + j] == lookahead_buffer[j]:
                j += 1

            if j > match_length:
                match_length = j
                match_distance = len(search_window) - i
                match_found = True

        if match_found:
            compressed_data.append((match_distance, match_length, lookahead_buffer[match_length]))
            pos += match_length + 1
        else:
            compressed_data.append((0, 0, data[pos]))
            pos += 1

    return compressed_data


def decompress_lz77(compressed_data):
    decompressed_data = ""
    for item in compressed_data:
        if item[0] == 0 and item[1] == 0:
            decompressed_data += item[2]
        else:
            start = len(decompressed_data) - item[0]
            for i in range(item[1]):
                decompressed_data += decompressed_data[start + i]
            decompressed_data += item[2]
    return decompressed_data


def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}
    result = []
    current_code = 256
    phrase = ""
    for symbol in data:
        if phrase + symbol in dictionary:
            phrase += symbol
        else:
            result.append(dictionary[phrase])
            dictionary[phrase + symbol] = current_code
            current_code += 1
            phrase = symbol
    if phrase in dictionary:
        result.append(dictionary[phrase])

    return result


def lzw_decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(256)}
    result = ""
    current_code = 256
    old_phrase = chr(compressed_data[0])
    result += old_phrase
    for code in compressed_data[1:]:
        if code in dictionary:
            new_phrase = dictionary[code]
        elif code == current_code:
            new_phrase = old_phrase + old_phrase[0]
        else:
            raise ValueError('Bad compressed sequence')

        result += new_phrase
        dictionary[current_code] = old_phrase + new_phrase[0]
        current_code += 1
        old_phrase = new_phrase

    return result


def evaluate_lz77(input_file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(input_file_path, 'r') as file:
            text = file.read()
        encoded_text = compress_lz77(text)
        with open(compressed_file_path, 'w') as output_file:
            value = json.dumps(encoded_text)
            output_file.write(value)
        print(f"Compression successful. Encoded file saved to {compressed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        with open(compressed_file_path, 'r') as file:
            encoded_text = file.read()
        decoded_text = decompress_lz77(json.loads(encoded_text))
        with open(reconstructed_file_path, 'w') as output_file:
            output_file.write(decoded_text)
        print(f"Decompression successful. Decoded file saved to {reconstructed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def evaluate_lzw(input_file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(input_file_path, 'r') as file:
            data = file.read()
        compressed_data = lzw_compress(data)
        with open(compressed_file_path, 'wb') as file:
            for code in compressed_data:
                file.write(code.to_bytes(2, 'big')) 
        print('File compressed successfully!')
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        with open(compressed_file_path, 'rb') as file:
            compressed_data = []
            while True:
                two_bytes = file.read(2)
                if not two_bytes:
                    break
                code = int.from_bytes(two_bytes, 'big')
                compressed_data.append(code)
        decompressed_data = lzw_decompress(compressed_data)
        with open(reconstructed_file_path, 'w') as file:
            file.write(decompressed_data)
        print('File decompressed successfully!')
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def compress_and_decompress(file_path, algo):
    extension = file_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    reconstructed_file_path = os.path.join(script_directory, 'reconstructed_'+algo+'.'+extension)

    if algo == 'LZ77':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.txt')
        evaluate_lz77(file_path, compressed_file_path, reconstructed_file_path)
    
    elif algo == 'LZW':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.lzw')
        evaluate_lzw(file_path, compressed_file_path, reconstructed_file_path)
    

    original_size = os.path.getsize(
        os.path.join(file_path)
    )
    compressed_size = os.path.getsize(
        os.path.join(compressed_file_path)
    )

    final_size = os.path.getsize(
        os.path.join(reconstructed_file_path)
    )
    
    loss_percentage =  (original_size - final_size)/ original_size
    reconstructed_file_path=reconstructed_file_path
    compressed_file_path=compressed_file_path
    compression_ratio = original_size/compressed_size  if compressed_size > 0 else 0

    return compression_ratio, loss_percentage, reconstructed_file_path, compressed_file_path


def main_data(data_path):
    algorithms = ['LZ77', 'LZW']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(data_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)

    return results
