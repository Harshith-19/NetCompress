from PIL import Image
import os

def evaluate_image(input_image_path, compression_method='DCT', quality=50):
    extension = input_image_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    output_path = os.path.join(script_directory, 'compressed.'+extension)
    try:
        img = Image.open(input_image_path)

        if compression_method == 'DCT':
            img.save(output_path, quality=quality)

        elif compression_method == 'Deflate':
            img.save(output_path, compress_level=9)

        else:
            print("Unsupported compression method.")

    except FileNotFoundError:
        print("The input image file was not found.")

    reconstructed_path = os.path.join(script_directory, 'reconstructed.'+extension)

    try:
        img = Image.open(output_path)
        img.save(reconstructed_path)
        print("Image reconstructed successfully!")

    except FileNotFoundError:
        print("The compressed image file was not found.")
    
    original_size = os.path.getsize(
        os.path.join(input_image_path)
    )
    compressed_size = os.path.getsize(
        os.path.join(output_path)
    )

    final_size = os.path.getsize(
        os.path.join(reconstructed_path)
    )
    # Check if decompressed directories exist before calculating losses
    loss_percentage =  (original_size - final_size)/ original_size
    reconstructed_file_path=reconstructed_path
    compressed_file_path=output_path
    compression_ratio = original_size/compressed_size  if compressed_size > 0 else 0

    return compression_ratio, loss_percentage, reconstructed_file_path, compressed_file_path


def main_image(image_path):
    algorithms = ['DCT', 'Deflate']
    results = []

    for algo in algorithms:
        result = evaluate_image(image_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)
    
    return results