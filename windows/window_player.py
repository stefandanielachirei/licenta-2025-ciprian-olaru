import cv2
import tkinter as tk
import time
from threading import Thread
from PIL import Image, ImageTk
import os

class VideoPlayer:
    def __init__(self, root, video_files, delay_between_videos=2):
        self.root = root
        self.video_files = video_files
        self.delay_between_videos = delay_between_videos
        self.current_video_index = 0
        self.is_playing = False
        self.cap = None
        self.should_stop = False

        self.canvas_width = 640
        self.canvas_height = 480

        self.root.title("Video Player")
        self.root.geometry(f"{self.canvas_width}x{self.canvas_height}")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.playback_thread = Thread(target=self.play_videos)
        self.playback_thread.daemon = True
        self.playback_thread.start()

    def play_videos(self):
        self.is_playing = True

        while self.current_video_index < len(self.video_files) and not self.should_stop:
            video_path = self.video_files[self.current_video_index]

            self.play_single_video(video_path)

            self.current_video_index += 1

            if self.current_video_index < len(self.video_files) and not self.should_stop:
                time.sleep(self.delay_between_videos)

        if not self.should_stop:
            self.root.after(100, self.root.quit)

        self.is_playing = False

    def play_single_video(self, video_path):
        try:
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                print(f"Error: Could not open video {video_path}")
                return

            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_delay = 1 / fps if fps > 0 else 0.03

            while self.cap.isOpened() and not self.should_stop:
                start_time = time.time()

                ret, frame = self.cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                original_height, original_width = frame_rgb.shape[:2]
                scale = min(self.canvas_width / original_width, self.canvas_height / original_height)
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))

                img = Image.fromarray(frame_resized)
                img_tk = ImageTk.PhotoImage(image=img)

                self.root.after_idle(self.update_canvas, img_tk, new_width, new_height)

                elapsed_time = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed_time)
                time.sleep(sleep_time)

            if self.cap:
                self.cap.release()
                self.cap = None

        except Exception as e:
            print(f"Error during video playback: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None

    def update_canvas(self, img_tk, img_width, img_height):
        self.img_tk = img_tk
        x_center = self.canvas_width // 2
        y_center = self.canvas_height // 2
        if not hasattr(self, 'image_id'):
            self.image_id = self.canvas.create_image(x_center, y_center, image=self.img_tk, anchor=tk.CENTER)
        else:
            self.canvas.itemconfig(self.image_id, image=self.img_tk)

    def on_closing(self):
        self.should_stop = True
        if self.cap:
            self.cap.release()
            self.cap = None
        self.root.destroy()

def launch_windows():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    video_files = [
        os.path.join(script_dir, "videos", "R.mp4"),
        os.path.join(script_dir, "videos", "U.mp4"),
        os.path.join(script_dir, "videos", "L.mp4")
    ]

    root = tk.Tk()
    player = VideoPlayer(root, video_files, delay_between_videos=1)
    root.mainloop()

    print("Video playback complete")
