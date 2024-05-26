import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для обработки видео")
        self.video_path = None
        self.cap = None
        self.original_frame = None
        self.label = tk.Label(self.root)
        self.label.pack()
        self.btn_load_video = tk.Button(self.root, text="Загрузить видео", command=self.load_video)
        self.btn_load_video.pack()
        self.btn_subtract_bg = tk.Button(self.root, text="Вычесть фон", command=self.subtract_background)
        self.btn_subtract_bg.pack(side=tk.LEFT)
        self.btn_blur_moving_objects = tk.Button(self.root, text="Размыть движущиеся объекты", command=self.blur_moving_objects)
        self.btn_blur_moving_objects.pack(side=tk.LEFT)
        self.btn_default = tk.Button(self.root, text="По умолчанию", command=self.display_default_video)
        self.btn_default.pack()

    def load_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.original_frame = self.get_frame()

    def subtract_background(self):
        if self.cap is not None:
            fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output_subtract_bg.mp4', fourcc, self.cap.get(cv2.CAP_PROP_FPS), 
                                  (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            while True:
                frame = self.get_frame()
                if frame is None:
                    break
                fgmask = fgbg.apply(frame)
                processed_frame = cv2.bitwise_and(frame, frame, mask=fgmask)
                out.write(processed_frame)
            out.release()

    def blur_moving_objects(self):
        if self.cap is not None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output_blur_moving_objects.mp4', fourcc, self.cap.get(cv2.CAP_PROP_FPS), 
                                  (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            while True:
                frame = self.get_frame()
                if frame is None:
                    break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (35, 35), 0)
                processed_frame = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
                out.write(processed_frame)
            out.release()

    def display_default_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        self.original_frame = self.get_frame()
        self.display_frame()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    def display_frame(self):
        if self.original_frame is not None:
            frame = cv2.cvtColor(self.original_frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame_tk = ImageTk.PhotoImage(frame)
            self.label.configure(image=frame_tk)
            self.label.image = frame_tk
            self.root.after(10, self.display_frame)

root = tk.Tk()
app = VideoProcessingApp(root)
root.mainloop()