from collections import defaultdict
import heapq


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


def compress(text):
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


def decompress(text, huffman_tree):
    huffman_decoded = huffman_decoding(text, huffman_tree)
    original_text = inverse_burrows_wheeler_transform(huffman_decoded)
    return original_text


def main(text):
    print(text)
    compressed_text, huffman_tree = compress(text)
    print(compressed_text)
    original_text = decompress(compressed_text, huffman_tree)
    print(original_text)