import subprocess
import os


class SP3:
    def __init__(self):
        pass

    @staticmethod
    def ex1(input_v):
        output1 = "BBB_720p.mpg"
        output2 = "BBB_480p.mpg"
        output3 = "BBB_240p.mpg"
        output4 = "BBB_120p.mpg"
        outputs = [output1, output2, output3, output4]

        command1 = ["ffmpeg", "-i", input_v, "-vf", "scale=1280:720", output1]
        command2 = ['ffmpeg', '-i', input_v, '-vf', 'scale=854:480', output2]
        command3 = ['ffmpeg', '-i', input_v, '-vf', 'scale=360:240', output3]
        command4 = ['ffmpeg', '-i', input_v, '-vf', 'scale=160:120', output4]

        if not os.path.exists(output1):
            subprocess.run(command1)
        if not os.path.exists(output2):
            subprocess.run(command2)
        if not os.path.exists(output3):
            subprocess.run(command3)
        if not os.path.exists(output4):
            subprocess.run(command4)

        option = int(input("Which resolution shall we convert to VP8?\n 1- 1280:720\n 2- 854:480\n 3- 360:240\n"
                           " 4- 160:120\n (Expected 1/2/3/4): "))
        cur_vid = outputs[option-1]
        print("Converting " + str(cur_vid) + " to VP8")
        vp8_com = ["ffmpeg", "-i", cur_vid, "-c:v", "libvpx", "-b:v", "1M", "-c:a", "libvorbis", "BBB_VP8.webm"]
        subprocess.run(vp8_com)

        option = int(input("Which resolution shall we convert to VP9?\n 1- 1280:720\n 2- 854:480\n 3- 360:240\n"
                           " 4- 160:120\n (Expected 1/2/3/4): "))
        cur_vid = outputs[option-1]
        print("Converting " + str(cur_vid) + " to VP9")
        vp9_com = ["ffmpeg", "-i", cur_vid, "-c:v", "libvpx-vp9", "-b:v", "1M", "-c:a", "libvorbis",
                   "BBB_VP9.webm"]
        subprocess.run(vp9_com)

        option = int(input("Which resolution shall we convert to h265?\n 1- 1280:720\n 2- 854:480\n 3- 360:240\n"
                           " 4- 160:120\n (Expected 1/2/3/4): "))
        cur_vid = outputs[option-1]
        print("Converting " + str(cur_vid) + " to h265")
        h265_com = ["ffmpeg", "-i", cur_vid, "-c:v", "libx265", "-crf", "28", "-c:a", "aac", "-b:a", "128k",
                    "BBB_h265.mp4"]
        subprocess.run(h265_com)

        opt = input("Converting to AV1 may take a very (extremely) long time. Would you like to do it anyway? (y/N)")
        if opt.lower() == 'y':
            option = int(input("Which resolution shall we convert to AV1?\n 1- 1280:720\n 2- 854:480\n 3- 360:240\n"
                               " 4- 160:120\n (Expected 1/2/3/4): "))
            cur_vid = outputs[option - 1]
            print("Converting " + str(cur_vid) + " to AV1")
            av1_com = ["ffmpeg", "-i", cur_vid, "-c:v", "libaom-av1", "-crf", "30", "-progress", "pipe:1",
                       "BBB_av1.mkv"]
            subprocess.run(av1_com)

    @staticmethod
    def ex2():
        videos = ["BBB_VP8.webm", "BBB_VP9.webm", "BBB_h265.mp4"]
        print("Which two coders shall we compare?\n 1- VP8\n 2- VP9\n 3- h265\n")
        cod1 = int(input("Coder 1 (Expected 1/2/3): "))
        cod2 = int(input("Coder 2 (Expected 1/2/3): "))

        command21 = ["ffmpeg", "-i", videos[cod1-1], "-i", videos[cod2-1], "-filter_complex", "[0:v][1:v]hstack[outv]",
                    "-map", "[outv]", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a",
                    "128k", "combined.mp4"]

        subprocess.run(command21)

        command22 = ["ffplay", "-i", "combined.mp4"]
        subprocess.run(command22)

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
    input_video = "BBB.mpg"
    sem3 = SP3()

    sem3.ex1(input_video)
    sem3.ex2()
