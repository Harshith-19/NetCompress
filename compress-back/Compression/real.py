import os
import brotli


def evaluate_brotli(input_file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(input_file_path, 'r') as file:
            text = file.read()
        text_bytes = text.encode('utf-8')
        compressed_data = brotli.compress(text_bytes)
        with open(compressed_file_path, 'wb') as output_file:
            output_file.write(compressed_data)
        print(f"Compression successful. Compressed file saved to {compressed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        with open(compressed_file_path, 'rb') as file:
            compressed_data = file.read()
        decompressed_data = brotli.decompress(compressed_data)
        decompressed_text = decompressed_data.decode('utf-8')
        with open(reconstructed_file_path, 'w') as output_file:
            output_file.write(decompressed_text)
        print(f"Decompression successful. Decompressed file saved to {reconstructed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def encode_rle(text):
    encoded_text = ""
    count = 1
    if not text:
        return text
    for i in range(len(text) - 1):
        if text[i] == text[i + 1]:
            count += 1
        else:
            encoded_text += str(count) + text[i]
            count = 1
    encoded_text += str(count) + text[-1]
    return encoded_text


def decode_rle(encoded_text):
    decoded_text = ""
    if not encoded_text:
        return encoded_text
    i = 0
    while i < len(encoded_text):
        count = int(encoded_text[i])
        char = encoded_text[i + 1]
        decoded_text += char * count
        i += 2    
    return decoded_text


def evaluate_rle(input_file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(input_file_path, 'r') as file:
            text = file.read()
        encoded_text = encode_rle(text)
        with open(compressed_file_path, 'w') as output_file:
            output_file.write(encoded_text)
        print(f"Compression successful. Encoded file saved to {compressed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        with open(compressed_file_path, 'r') as file:
            encoded_text = file.read()
        decoded_text = decode_rle(encoded_text)
        with open(reconstructed_file_path, 'w') as output_file:
            output_file.write(decoded_text)
        print(f"Decompression successful. Decoded file saved to {reconstructed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def compress_and_decompress(file_path, algo):
    extension = file_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    reconstructed_file_path = os.path.join(script_directory, 'reconstructed_'+algo+'.'+extension)
    compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.'+extension)

    if algo == 'Brotli':
        evaluate_brotli(file_path, compressed_file_path, reconstructed_file_path)
    
    elif algo == 'RLE':
        evaluate_rle(file_path, compressed_file_path, reconstructed_file_path)
    

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


def main_real(real_time_path):
    algorithms = ['Brotli', 'RLE']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(real_time_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)

    return results
