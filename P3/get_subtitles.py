import yt_dlp
import subprocess


def download_subtitles(video_url):  # Downloading subtitles from a YouTube URL
    options = {
        'format': 'best',
        'writesubtitles': True,
        'subtitleslangs': ['es'],
        'skip_download': True,
        'postprocessors': [{
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        }],
        'outtmpl': 'rajoy_subtitles.srt',
        'writeautomaticsub': 'rajoy_subtitles.srt',
        'verbose': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    return


def add_subtitles(video_file, subtitle_file):

    command = ['ffmpeg', '-i', video_file, '-i', subtitle_file, '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'mov_text',
               '-map', '0', '-map', '1', '-metadata:s:s:0', 'language=spa', 'rajoy_subtitles.mp4']
    # Command for adding subtitles to a video
    subprocess.run(command)
