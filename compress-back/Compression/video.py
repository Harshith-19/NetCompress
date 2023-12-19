import os
import ffmpeg
from moviepy.editor import VideoFileClip


def compress_and_decompress(file_path, algo):
    extension = file_path.split('.')[-1]
    script_directory = os.path.dirname(__file__)
    reconstructed_file_path = os.path.join(script_directory, 'reconstructed_'+algo+'.'+extension)

    if algo == 'H.264':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.'+extension)
        ffmpeg.input(file_path).output(compressed_file_path, vcodec='libx264', crf=23).run()
        reconstructed_video = VideoFileClip(compressed_file_path)
        reconstructed_video.write_videofile(reconstructed_file_path)
        reconstructed_video.close()
    
    elif algo == 'H.265':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.'+extension)
        ffmpeg.input(file_path).output(compressed_file_path, vcodec='libx265', crf=28).run()
        reconstructed_video = VideoFileClip(compressed_file_path)
        reconstructed_video.write_videofile(reconstructed_file_path)
        reconstructed_video.close()
    
    elif algo == 'VP9':
        compressed_file_path = os.path.join(script_directory, 'compressed_'+algo+'.webm')
        ffmpeg.input(file_path).output(compressed_file_path, vcodec='libvpx-vp9').run()
        ffmpeg.input(compressed_file_path).output(reconstructed_file_path, vcodec='copy', acodec='copy').run()
    

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



def main_video(video_path):
    algorithms = ['H.264', 'H.265', 'VP9']
    results = []

    for algo in algorithms:
        result = compress_and_decompress(video_path, algo)
        result_dict = {
            "algorithm" : algo,
            "compressed_file_path" : result[3],
            "reconstructed_file_path" : result[2],
            "compression_ratio" : result[0],
            "loss_percentage" : result[1],
        }
        results.append(result_dict)

    return results
