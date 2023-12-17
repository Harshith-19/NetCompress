import os
import shutil
import lzma
import zipfile
import tempfile

def compress_and_decompress(folder_path, algo):
    script_directory = os.path.dirname(__file__)

    if algo=="lzma":
        archive = os.path.join(script_directory, 'compressed_lzma.xz')
        with lzma.open(archive, 'wb', preset=9) as lzma_file:
            # Compress the contents of the folder directly
            shutil.make_archive(os.path.splitext(archive)[0], 'zip', folder_path)
    
        # Decompress using LZMA2
        decompressed_dir = tempfile.mkdtemp()
        archive = os.path.join(script_directory, 'compressed_lzma.zip')
        with zipfile.ZipFile(archive, 'r', zipfile.ZIP_DEFLATED) as lzma_zip:
            lzma_zip.extractall(decompressed_dir)
        
        
    elif algo=="deflate":
        archive = os.path.join(script_directory, 'compressed_deflate.zip')
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as deflate_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    deflate_file.write(file_path, arcname=arcname)


        # Decompress using Deflate
        decompressed_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, 'r', zipfile.ZIP_DEFLATED) as deflate_zip:
            deflate_zip.extractall(decompressed_dir)
    
    # Calculate compression ratios and losses
    original_size = sum(os.path.getsize(os.path.join(root, file))
                        for root, _, files in os.walk(folder_path) for file in files)
    compressed_size = os.path.getsize(
        os.path.join(archive)
    )

    final_size=sum(os.path.getsize(os.path.join(root, file))
                        for root, _, files in os.walk(decompressed_dir) for file in files)
    # Check if decompressed directories exist before calculating losses
    loss_percentage =  (original_size - final_size)/ original_size
    reconstructed_file_path=decompressed_dir
    compressed_file_path=archive
    compression_ratio = original_size/compressed_size  if compressed_size > 0 else 0

    return compression_ratio, loss_percentage, reconstructed_file_path, compressed_file_path

def main(folder_path):
    algorithms = ['lzma', 'deflate']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(folder_path, algo)
        results.append(result)

    return results

if __name__ == "__main__":
    # Example usage
    folder_path = input("Enter folder path: ")
    compression_results = main(folder_path)

    for i, result in enumerate(compression_results, 1):
        print(f"\nAlgorithm {i}:")
        print(f"Compressed File Path: {result[3]}")  # Using positional indexing
        print(f"Reconstructed File Path: {result[2]}")  # Using positional indexing
        print(f"Compression Ratio: {result[0]:.2f}")  # Using positional indexing
        print(f"Loss Percentage: {result[1] * 100:.2f}%")  # Using positional indexing

