from yt_dlp import YoutubeDL

from core.conf import Config

def testhook(data) -> None:
    print("ARGS:", data.get('total_bytes_estimate'),
          f"{data.get('fragment_index')}/{data.get('fragment_count')}",
          "|elapsed:", data.get('elapsed'),
          "|status:", data.get('status'),
          '|max_progress:', data.get('max_progress'),
          '|progress_idx:', data.get('progress_idx')
          )


def youtube_download(urls: list[str], hook: callable = None):
    """download youtube video"""
    conf = Config()

    params = {
        'proxy': conf.settings['proxy'],
        'windowsfilenames': True,
        'progress_hooks': [testhook, hook],
        'quiet': True,
        'logger': None
        # 'logtostderr': None
    }

    with YoutubeDL(params) as ytdl:
        return ytdl.download(urls)

"""
yt = YoutubeDL(params)
yt.download(['https://www.youtube.com/watch?v=moQ9BtCX3f8'])
"""
