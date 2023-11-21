import ffmpeg
import os
import subprocess
from get_subtitles import download_subtitles, add_subtitles
from yuv_hist import video_with_hist


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
    def ex2(or_v):  # Getting a 50-second video
        start = '00:02:03'
        end = '00:02:53'
        (
            ffmpeg.input(or_v, ss=start, to=end)
            .output("BBB_50s.mpg")
            .run()
        )
        command21 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-c', 'copy', '-an', 'mute_BBB.mpg']
        subprocess.run(command21)   # Mute video

        command22 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-ac', '1', 'mono.mp3']
        subprocess.run(command22)   # Mono audio

        command23 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-b:a', '32k', 'stereo.mp3']
        subprocess.run(command23)   # Stereo audio

        command24 = ['ffmpeg', '-i', 'BBB_50s.mpg', '-c:a', 'aac', 'audio.aac']
        subprocess.run(command24)   # AAC audio file

        command25 = ['ffmpeg', '-i', 'mute_BBB.mpg', '-i', 'mono.mp3', '-i', 'stereo.mp3', '-i',
                     'audio.aac', '-map', '0', '-map', '1:a', '-map', '2:a', '-map', '3:a', '-c:v', 'copy', '-c:a:0',
                     'copy', '-c:a:1', 'copy', '-c:a:2', 'copy', '-shortest', 'container_output.mp4']

        subprocess.run(command25)   # Adding everything inside a mp4 container

        return

    @staticmethod
    def ex3(file_path):     # Counting number of tracks in mp4 container
        command3 = ['ffmpeg', '-i', file_path]
        result = subprocess.run(command3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_lines = result.stderr.split('\n')
        track_count = 0
        for line in output_lines:
            if 'Stream #' in line:
                track_count += 1

        print("There are a total of " + str(track_count) + " tracks in the mp4 container.\n")
        return


if __name__ == '__main__':
    # Initializing
    original_video = 'BBB.mpg'		# To be included in the folder!!
    input_vid = 'rajoy.mp4'
    video_link = "https://www.youtube.com/watch?v=glMm5w7K4Yg"
    exercise = '0'
    container = 'container_output.mp4'
    subtitles_file = "rajoy_subtitles.srt.es.vtt"
    p3 = Practice3()

    if not os.path.exists('BBB.mpg'):
        print("Please make sure BBB.mpg exists in the current folder,\n"
              "Otherwise the script does not work.\n")
    else:
        while exercise != 'EXIT':
            exercise = input('Which exercise shall we solve now? Expected integer from 1 to 6, '
                             'EXIT to end the program\n')

            if exercise == '1':
                if not os.path.exists('BBB_9s.mpg'):  # Only trims if it has not been converted yet
                    start_time = '00:01:46'
                    end_time = '00:01:56'
                    (
                        ffmpeg.input(original_video, ss=start_time, to=end_time)
                        .output("BBB_9s.mpg")
                        .run()
                    )
                video_9s = 'BBB_9s.mpg'
                p3.ex1(video_9s)

            elif exercise == '2':
                p3.ex2(original_video)
                print("Mute video and mono, stereo and AAC-format files created correctly.\n")
                print("mp4 container created correctly.\n")

            elif exercise == '3':
                if not os.path.exists(container):
                    print('You should run Exercise 2 first.\n')
                else:
                    p3.ex3(container)

            elif exercise == '4' or exercise == '5':
                download_subtitles(video_link)
                if os.path.exists(subtitles_file):
                    add_subtitles(input_vid, subtitles_file)
                    print("Subtitles added to the original video correctly. Check rajoy_subtitles.mp4\n"
                          "WARNING!!: The speech may cause irreversible brain damage, and it \n"
                          "is impossible to understand even with subtitles.\n")
                else:
                    print("Error creating subtitles file. Please try again\n")

            elif exercise == '6':
                video_with_hist(input_vid)
                print("Histogram video created correctly. Check rajoy_hist.mp4\n")
            elif exercise.upper() == 'EXIT':
                print('See you soon!\n')
                break
            else:
                print('Invalid input, please try again.\n')

