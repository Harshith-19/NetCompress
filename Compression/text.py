from collections import defaultdict
import heapq
import os
import bz2


#BWT to transform data
def burrows_wheeler_transform(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    sorted_rotations = sorted(rotations)
    bwt = ''.join(rot[-1] for rot in sorted_rotations)    
    return bwt


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_dict):
    priority_queue = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0]


def generate_codes(root, current_code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
        return
    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)


def huffman_encoding(text):
    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1
    huffman_tree = build_huffman_tree(freq_dict)
    codes = {}
    generate_codes(huffman_tree, "", codes)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, huffman_tree


def compress_huffman(text):
    text += "$"
    bwt_text = burrows_wheeler_transform(text)
    huffman_text, huffman_tree = huffman_encoding(bwt_text)
    return huffman_text, huffman_tree


#Inverse BWT to reconstruct original data
def inverse_burrows_wheeler_transform(bwt):
    table = [''] * len(bwt)    
    for i in range(len(bwt)):
        table = sorted([bwt[i] + table[i] for i in range(len(bwt))])
    original_text = [s for s in table if s.endswith('$')][0]    
    return original_text.rstrip('$')


def huffman_decoding(encoded_text, root):
    decoded_text = ""
    current = root
    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            decoded_text += current.char
            current = root
    return decoded_text


def decompress_huffman(text, huffman_tree):
    huffman_decoded = huffman_decoding(text, huffman_tree)
    original_text = inverse_burrows_wheeler_transform(huffman_decoded)
    return original_text


def evaluate_huffman(file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        compressed_text, huffman_tree = compress_huffman(text)
        binary_data = int(compressed_text, 2).to_bytes((len(compressed_text) + 7) // 8, byteorder='big')
        with open(compressed_file_path, 'wb') as output_file:
            output_file.write(binary_data)
        print(f"Compression successful. Encoded file saved to {compressed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        with open(compressed_file_path, 'rb') as file:
            encoded_text = file.read()
        encoded_text = ''.join(format(byte, '08b') for byte in encoded_text)
        original_text = decompress_huffman(encoded_text, huffman_tree)
        with open(reconstructed_file_path, 'w') as output_file:
            output_file.write(original_text)
        print(f"Decompression successful. Decoded file saved to {reconstructed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def evaluate_bzip2(file_path, compressed_file_path, reconstructed_file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read().encode('utf-8')
        compressed_data = bz2.compress(text)
        with open(compressed_file_path, 'wb') as output_file:
            output_file.write(compressed_data)
        print(f"Compression successful. Encoded file saved to {compressed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    try:
        with open(compressed_file_path, 'rb') as file:
            encoded_text = file.read()
        original_text = bz2.decompress(encoded_text).decode('utf-8')
        with open(reconstructed_file_path, 'w') as output_file:
            output_file.write(original_text)
        print(f"Decompression successful. Decoded file saved to {reconstructed_file_path}")
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def compress_and_decompress(file_path, algo):
    extension = file_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    reconstructed_file_path = os.path.join(script_directory, 'reconstructed_'+algo+'.'+extension)

    if algo == 'Huffman':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.bin')
        evaluate_huffman(file_path, compressed_file_path, reconstructed_file_path)
    
    elif algo == 'BZIP':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.bz2')
        evaluate_bzip2(file_path, compressed_file_path, reconstructed_file_path)
    

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


def main(text_path):
    algorithms = ['Huffman', 'BZIP']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(text_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)

    return results

