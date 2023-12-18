import os
import subprocess
from pydub import AudioSegment

def compress_and_decompress(file_path, algo):
    extension = file_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    reconstructed_file_path = os.path.join(script_directory, 'reconstructed_'+algo+'.'+extension)

    if algo == 'AAC':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.aac')
        command = ['ffmpeg','-i', file_path, '-c:a', 'aac', '-strict', 'experimental', compressed_file_path]
        subprocess.run(command, check=True)
        audio = AudioSegment.from_file(compressed_file_path, format='aac')
        audio.export(reconstructed_file_path, format=extension)
    
    elif algo == 'FLAC':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.flac')
        audio = AudioSegment.from_file(file_path)
        audio.export(compressed_file_path, format='flac')
        audio = AudioSegment.from_file(compressed_file_path, format='flac')
        audio.export(reconstructed_file_path, format=extension)
    
    elif algo == 'ALAC':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.m4a')
        ffmpeg_cmd = ["ffmpeg","-i", file_path, "-codec:a", "alac", compressed_file_path ]
        subprocess.run(ffmpeg_cmd)
        audio = AudioSegment.from_file(compressed_file_path, format='m4a')
        audio.export(reconstructed_file_path, format=extension)      

    
    original_size = os.path.getsize(
        os.path.join(file_path)
    )
    compressed_size = os.path.getsize(
        os.path.join(compressed_file_path)
    )

    final_size = os.path.getsize(
        os.path.join(reconstructed_file_path)
    )
    # Check if decompressed directories exist before calculating losses
    loss_percentage =  (original_size - final_size)/ original_size
    reconstructed_file_path=reconstructed_file_path
    compressed_file_path=compressed_file_path
    compression_ratio = original_size/compressed_size  if compressed_size > 0 else 0

    return compression_ratio, loss_percentage, reconstructed_file_path, compressed_file_path



def main_audio(audio_path):
    algorithms = ['AAC', 'FLAC', 'ALAC']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(audio_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)

    return results