import ffmpeg
import os
import subprocess


class Practice3:
    def __init__(self):
        pass

    @staticmethod
    def ex1(input_v):      # Showing macro-blocks and vectors
        command11 = ['ffplay', '-flags2', '+export_mvs', input_v, '-vf', 'codecview=mv=pf+bf+bb']
        command12 = ['ffmpeg', '-flags2', '+export_mvs', '-i', input_v, '-vf', 'codecview=mv=pf+bf+bb',
                     'motion_BBB.mpg']
        subprocess.run(command11)
        subprocess.run(command12)
        return

    @staticmethod
    def ex2(or_v):
        start = '00:02:03'
        end = '00:02:53'
        (
            ffmpeg.input(or_v, ss=start, to=end)
            .output("BBB_50s.mpg")
            .run()
        )
        command21 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-c', 'copy', '-an', 'mute_BBB.mpg']
        subprocess.run(command21)

        command22 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-ac', '1', 'mono.mp3']
        subprocess.run(command22)

        command23 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-b:a', '32k', 'stereo.mp3']
        subprocess.run(command23)

        command24 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-c:a', 'aac', 'audio.aac']
        subprocess.run(command24)

        command25 = ['ffmpeg', '-i', 'mute_BBB.mpg', '-i', 'mono.mp3', '-i', 'stereo.mp3', '-i', 'audio.aac', '-c',
                     'copy', 'container_output.mp4']
        subprocess.run(command25)

        output = 'container_output.mp4'
        return output

    @staticmethod
    def ex3(mp4_vid):
        command31 = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of',
        'default=noprint_wrappers=1:nokey=1', mp4_vid]
        subprocess.run(command31)
        command32 = ['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=codec_type', '-of',
        'default=noprint_wrappers=1:nokey=1', mp4_vid]
        subprocess.run(command32)

        # Run the commands and capture the output
        proc_audio = subprocess.Popen(command31, stdout=subprocess.PIPE)
        proc_video = subprocess.Popen(command32, stdout=subprocess.PIPE)

        # Read and print the output
        output_audio = proc_audio.stdout.read()
        output_video = proc_video.stdout.read()

        print(output_audio.decode('utf-8'))
        print(output_video.decode('utf-8'))
        return


if __name__ == '__main__':
    original_video = 'BBB.mpg'
    if not os.path.exists('BBB_9s.mpg'):  # Only trims if it has not been converted yet
        start_time = '00:01:46'
        end_time = '00:01:56'
        (
            ffmpeg.input(original_video, ss=start_time, to=end_time)
            .output("BBB_9s.mpg")
            .run()
        )

    video_9s = 'BBB_9s.mpg'

    p3 = Practice3()
    # p3.ex1(video_9s)
    video_mp4_dir = p3.ex2(original_video)
    p3.ex3(video_mp4_dir)
