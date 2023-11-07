from P1.rgb_yuv import Practice1
import subprocess
import cv2
import os
import sys
sys.path.append('/P1')


class Practice2(Practice1):
    @staticmethod
    def ex1(input_video):
        command1 = ['ffmpeg', '-i', input_video, '-c:v', 'mpeg2video', '-q:v', '6', '-c:a', 'mp2', 'BBB.mpg']
        subprocess.run(command1)
        print('Video converted')
        return

    @staticmethod
    def ex1_2(input_video):
        output_folder = 'ex1_frames/'
        cap = cv2.VideoCapture(input_video)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        os.makedirs(output_folder, exist_ok=True)

        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

            # Save frame as image
            frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

            # Save information (frame number and timestamp)
            info_filename = os.path.join(output_folder, f"frame_{frame_number:04d}_info.txt")
            with open(info_filename, 'w') as f:
                f.write(f"Frame number: {frame_number}\n")
                f.write(f"Timestamp (ms): {timestamp}\n")
                f.write(f"FPS: {fps}\n")
        cap.release()
        print('Video parsed')
        return

    @staticmethod
    def ex2(input_video):
        command21 = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of',
                     'csv=s=x:p=0', input_video]
        print('Current resolution: ')
        subprocess.run(command21)

        command2 = ['ffmpeg', '-i', 'BBB.mpg', '-vf', 'scale=-2:720', 'BBB_720.mpg']
        subprocess.run(command2)
        print('Resolution updated to ')
        subprocess.run(command21)
        return

    @staticmethod
    def ex3(input_video):

        command3 = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=pix_fmt',
                    '-of', 'default=noprint_wrappers=1:nokey=1', input_video]
        print('Current chroma subsampling:')
        subprocess.run(command3)
        command4 = ['ffmpeg', '-i', 'BBB.mpg', '-vf', 'format=yuv422p', 'BBB_yuv422p.mpg']
        subprocess.run(command4)
        print('Chroma subsampling updated to yuv422p')
        return

    @staticmethod
    def ex4(input_video):
        cap = cv2.VideoCapture(input_video)

        properties = {
            "Frame Count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "Duration (seconds)": int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)),
            "Frame Width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "Frame Height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "Frames Per Second (FPS)": int(cap.get(cv2.CAP_PROP_FPS)),
            "Codec": int(cap.get(cv2.CAP_PROP_FOURCC)),
            "Bit Rate (kbps)": int(cap.get(cv2.CAP_PROP_BITRATE)),
            "Is Color": cap.get(cv2.CAP_PROP_CONVERT_RGB),
        }

        cap.release()

        return properties


if __name__ == '__main__':

    p2 = Practice2()
    exercise = '0'

    video_mp4 = 'BBB.mp4'
    if not os.path.exists('BBB.mpg'):
        p2.ex1(video_mp4)

    video_mpg = 'BBB.mpg'

    while exercise != 'EXIT':
        exercise = input('Which exercise shall we solve now? Expected integer from 1 to 5'
                         ' (Exercise 1.1 was already executed to obtain BBB.mpg), '
                         'EXIT to end the program\n')

        if exercise == '1':
            p2.ex1_2(video_mpg)

        elif exercise == '2':
            p2.ex2(video_mpg)
        elif exercise == '3':
            p2.ex3(video_mpg)

        elif exercise == '4':
            video_info = p2.ex4(video_mpg)

            for key, value in video_info.items():
                print(f'{key}: {value}')
        elif exercise == '5':
            ans = input('Would you like to run Practice1?(Y/N) ')
            if ans.upper() == 'Y':
                p2.launch()
            elif ans.upper() == 'N':
                print('OK, as you wish')
            else:
                print('Invalid input, please try again.')

        elif exercise.upper() == 'EXIT':
            print('See you soon!')
            break
        else:
            print('Invalid input, please try again.')



