import subprocess
import cv2
import os


def parse_video(input_video_path, output_folder):
    cap = cv2.VideoCapture(input_video_path)
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
    return


if __name__ == '__main__':

    command1 = ['ffmpeg', '-i', 'BBB.mp4', '-c:v', 'mpeg2video', '-q:v', '6', '-c:a', 'mp2', 'BBB.mpg']

    # subprocess.run(command1)
    print('Video converted')

    # parse_video('BBB.mpg', 'ex1_frames/')

    command2 = ['ffmpeg', '-i', 'BBB.mpg', '-vf', 'scale=-2:720', 'BBB_720.mpg']
    subprocess.run(command2)
