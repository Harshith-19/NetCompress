import sys
from PIL import Image

def compress_image(input_image_path, output_image_path, compression_method='DCT', quality=50):
    try:
        img = Image.open(input_image_path)

        if compression_method == 'DCT':
            img.save(output_image_path, quality=quality)

        elif compression_method == 'Deflate':
            img.save(output_image_path, compress_level=9)

        else:
            print("Unsupported compression method.")

    except FileNotFoundError:
        print("The input image file was not found.")

def reconstruct_image(compressed_image_path, output_reconstructed_image_path):
    try:
        img = Image.open(compressed_image_path)
        img.save(output_reconstructed_image_path)
        print("Image reconstructed successfully!")

    except FileNotFoundError:
        print("The compressed image file was not found.")

if __name__ == "__main__":
    action = input("Enter 'compress' to compress or 'decompress' to decompress: ")

    if action not in ['compress', 'decompress']:
        print("Invalid action. Use 'compress' or 'decompress'.")
        sys.exit(1)

    input_image_path = input("Enter the path of the input image file: ")
    output_file_path = input("Enter the path for the output file: ")

    if action == 'compress':
        compression_method = input("Enter compression method (DCT/Deflate): ")
        quality_level = 50  
        compress_image(input_image_path, output_file_path, compression_method, quality_level)
    
    elif action == 'decompress':
        reconstruct_image(input_image_path, output_file_path)
