import subprocess


def video_with_hist(input_file):    # Creating video with YUV histogram displayed
    command = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex', "[0:v]split=2[a][b];[b]histogram,format=yuva444p[hh];[a][hh]overlay",
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'veryfast',
        '-c:a', 'aac',
        'rajoy_hist.mp4'
    ]

    subprocess.run(command)
