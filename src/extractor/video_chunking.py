from pytubefix import YouTube
from pytubefix.cli import on_progress
import cv2
import pysrt

import os

class VideoChunking:
    @staticmethod
    def download_url(url:str, dir:str='./data/video') -> tuple[str, str]:
        yt = YouTube(url, on_progress_callback=on_progress)
        title = yt.title[:15].strip()
        video_dir = os.path.join(dir, title)
        os.makedirs(video_dir, exist_ok=True)

        print(f"Downloading video {title}...")
        ys = yt.streams.get_highest_resolution() # it returns the resolution of 360p anyway
        ys.download(video_dir, filename=f'{title}.mp4')

        caption = yt.captions[yt.caption_tracks[0].code]
        caption.save_captions(os.path.join(video_dir, f"{title}.srt"))
        print('~'*80)

        return os.path.join(video_dir, f"{title}.mp4"), os.path.join(video_dir, f"{title}.srt")

    @staticmethod
    def get_video_chunk(video_path:str, sub_path:str) -> list[dict]:
        video = cv2.VideoCapture(video_path)
        trans = pysrt.open(sub_path)

        frame_dir = os.path.join(os.path.dirname(video_path), 'frames')
        os.makedirs(frame_dir, exist_ok=True)

        meta_data = []

        for idx, transcript in enumerate(trans):
            # get the start time and end time in seconds
            start = transcript.start
            start = (start.minutes*60 + start.seconds)*1000 + start.milliseconds

            end = transcript.end
            end = (end.minutes*60 + end.seconds)*1000 + end.milliseconds
            # print(start, end)

            mid = (start+end)/2
            video.set(cv2.CAP_PROP_POS_MSEC, mid)
            success, frame = video.read()

            if success:
                img_path = os.path.join(frame_dir, f'f_{idx}.jpeg')
                cv2.imwrite(img_path, frame)

                meta_data.append({
                    'extracted_frame_path': img_path,
                    'transcript': transcript.text,
                    'video_segment_id': idx,
                    # 'video_path': path_to_video,
                    'mid_time_ms': mid,
                })

        return meta_data

if __name__=='__main__':
    video_path, sub_path = VideoChunking.download_url('https://www.youtube.com/watch?v=alDhOLhbkbY')
    VideoChunking.get_video_chunk(video_path, sub_path)

