import yt_dlp
import itertools
import threading
import time
from colorama import Fore, init
import pyfiglet

init(autoreset=True)
print(pyfiglet.figlet_format("YouTube D"))
def spinning_cursor():
    for cursor in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        print(f'\r{Fore.CYAN}Searching {cursor}', end='', flush=True)
        time.sleep(0.1)

def find_video_info(video_url):
    global loading
    loading = True
    spinner = threading.Thread(target=spinning_cursor)
    spinner.start()
    
    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            loading = False
            available_formats = [
                (fmt['resolution'], fmt['format_id'])
                for fmt in info['formats']
                if fmt.get('resolution')
            ]
            if not available_formats:
                print(f"\n{Fore.RED}No formats available for this video.")
                return []
            
            print(f"\n{Fore.GREEN}Available Qualities:")
            for i, (resolution, format_id) in enumerate(available_formats):
                print(f"{Fore.YELLOW}{i + 1}. {resolution} ({format_id})")
            return available_formats
        except Exception as e:
            loading = False
            print(f"\n{Fore.RED}Error fetching video info")
            return []

def download_video(video_url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"{Fore.CYAN}Starting download...")
            ydl.download([video_url])
            print(f"{Fore.GREEN}Download completed!")
        except Exception as e:
            print(f"{Fore.RED}Error during download: {e}")

def hook(d):
    if d['status'] == 'downloading':
        percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        speed = d.get('speed', 0) / 1024
        downloaded_size = d.get('downloaded_bytes', 0) / 1024
        print(f"\r{Fore.BLUE}[Downloading] {percent:.2f}% of {downloaded_size:.2f}KiB at {speed:.2f}KiB/s", end='')

if __name__ == '__main__':
    while True:
        video_url = input(f"{Fore.CYAN}Enter the YouTube video URL: ")
        available_formats = find_video_info(video_url)
        if not available_formats:
            print(f"{Fore.RED}Process ended.")
        else:
            try:
                quality_choice = int(input(f"\n{Fore.CYAN}Enter the number for desired quality: "))
                selected_format_id = available_formats[quality_choice - 1][1]
                download_video(video_url, selected_format_id)
            except (IndexError, ValueError):
                print(f"{Fore.RED}Invalid input. Process cancelled.")
