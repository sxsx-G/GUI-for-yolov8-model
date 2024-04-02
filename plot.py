import cv2
import torch
from ultralytics import YOLO
from cv2 import getTickCount, getTickFrequency
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import os


device_name = None

def quit():
    os._exit(0)


class App:
    def __init__(self, root):
        self.thread = None
        self.save_dir = None
        self.model= None
        self.root = root
        self.root.title("YOLOv8 Class Detection")
        self.root.geometry('1080x600')
        self.cap = cv2.VideoCapture("video_file_path")
        self.use_fps_algorithm = False

        # 创建按钮框架，并放置在窗口顶部
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="top", fill="x")

        self.save_button = tk.Button(self.button_frame, text="选择结果保存路径", command=self.select_save_dir)
        self.save_button.pack(side="left")

        self.model_button = tk.Button(self.button_frame, text="选择模型", command=self.select_model, state="disabled")
        self.model_button.pack(side="left")

        self.stream_button = tk.Button(self.button_frame, text="选择视频源", command=self.select_source,
                                       state="disabled")
        self.stream_button.pack(side="left")

        self.start_button = tk.Button(self.button_frame, text="开始检测", command=self.start, state="disabled")
        self.start_button.pack(side="left")

        self.quit_button = tk.Button(self.button_frame, text="退出程序", command=quit, state="normal")
        self.quit_button.pack(side="left")

        # 创建一个Combobox控件来选择设备
        self.device_combobox = ttk.Combobox(self.button_frame, values=['cpu', 'cuda', 'mps'], state='disabled')
        self.device_combobox.set("选择设备")
        self.device_combobox.pack(side='left')
        self.device_combobox.bind('<<ComboboxSelected>>', self.select_device)

        self.info_text = tk.Text(self.button_frame, height=2,state='normal')
        self.info_text.insert(tk.END, "Steps:选择结果保存路径->选择模型->选择视频源->开始检测")
        self.info_text.pack(side='left')

        # 使用PanedWindow来改善布局
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.paned_window, width=450)  # 设置初始高度
        self.paned_window.add(self.image_frame, weight=1)  # 图像框架应该占用大部分空间

        self.total_time_frame = tk.Frame(self.paned_window, height=150, background="gray")
        self.total_time_text = tk.Text(self.total_time_frame)
        self.total_time_text.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.total_time_frame, weight=0)  # 总时间框架占用较少空间

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

    def select_source(self):
        # 选择视频源
        msg_box = messagebox.askquestion('选择视频源', 'yes：选择摄像头 no:选择视频', icon='warning')
        if msg_box == 'yes':
            self.cap = cv2.VideoCapture(0)
            self.use_fps_algorithm = True
        else:
            video_file_path = filedialog.askopenfilename()
            self.use_fps_algorithm = False
            if video_file_path:
                self.cap = cv2.VideoCapture(video_file_path)
                self.start_button.config(state="normal")
                with open(os.path.join(self.save_dir, 'cache.txt'), 'a') as f:
                    f.write(video_file_path + '\n')

            else:
                print("未选择文件，程序退出")
                exit(0)

        return self.cap

    def select_device(self, event):
        # Get the selected device from the combobox
        self.device_name = self.device_combobox.get()

        # Check if the device name is valid
        if self.device_name in ['cpu', 'cuda', 'mps']:
            # If the device name is valid, set the device
            messagebox.showinfo('设备选择', f'已选择{self.device_name}')
            self.start_button.config(state="normal")
        else:
            # If the device name is not valid, show an error message
            messagebox.showerror('错误', '无效的设备名称')

        # Update the model to use the selected device
        self.model.to(self.device_name)

    def load_cache(self):
        cache_file_path = os.path.join(self.save_dir, 'cache.txt')
        if os.path.exists(cache_file_path):
            try:
                with open(cache_file_path, 'r') as f:
                    lines = f.readlines()
                    model_file_path = lines[0].strip()
                    video_file_path = lines[1].strip()
                    self.model = YOLO(model_file_path)
                    self.cap = cv2.VideoCapture(video_file_path)
                    self.stream_button.config(state="normal")
                    self.quit_button.config(state="normal")
                    self.device_combobox.config(state="normal")
                    self.info_text.config(state="normal")
                    self.info_text.delete('1.0', tk.END)
                    self.info_text.insert(tk.END,"model:"+lines[0]+"video:"+lines[1])
            except:
                self.info_text.insert(tk.END, "缓存文件已损坏，请重新选择模型和视频源")
                with open(os.path.join(self.save_dir, 'cache.txt'), 'w') as f:
                    f.write('')

    def select_model(self):
        model_file_path = filedialog.askopenfilename()
        # 加载 YOLOv8 模型
        if model_file_path:
            try:
                self.model = YOLO(model_file_path)
                self.stream_button.config(state="normal")
                with open(os.path.join(self.save_dir, 'cache.txt'), 'a') as f:
                    f.write(model_file_path + '\n')
            except Exception as e:
                print(f"无法加载模型，错误信息：{e}")
                exit(0)
        else:
            print("未选择模型文件，程序退出")
            exit(0)

    def select_save_dir(self):
        save_dir = filedialog.askdirectory()
        if save_dir:
            self.save_dir = save_dir
            self.model_button.config(state="normal")
            self.load_cache()
        else:
            print("未选择保存路径，程序退出")
            exit(0)

    def save_total_time(self, total_counts_divided_str):
        with open(os.path.join(self.save_dir, 'total_time.txt'), 'w') as f:
            f.write(total_counts_divided_str)

    def start(self):

        # 获取视频的宽度和高度
        # width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = 800
        height = 700
        # 设置图像Frame的大小
        self.image_frame.config(width=int(width), height=int(height))
        self.stream_button.config(state="disabled")
        self.start_button.config(state="disabled")
        self.model_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.quit_button.config(state="normal")
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        # 创建一个字典来存储每个类别的名称
        class_names = {
            0: "playing_phone",
            1: "listening",
            2: "considering",
            3: "reading",
            4: "using_Laptop",
            5: "writing",
            6: "talking",
            7: "sleeping",
            8: "eating"
        }

        # 创建一个字典来存储每个类别的累计数量
        total_counts = {}

        # 创建一个字典来存储每个类别的累计时间
        total_times = {}

        while self.cap.isOpened():
            loop_start = getTickCount()
            success, frame = self.cap.read()  # 读取摄像头的一帧图像

            if success:
                results = self.model.predict(source=frame, device=self.device_name)  # 对当前帧进行目标检测并显示结果
                annotated_frame = results[0].plot()

                for r in results:
                    boxes = r.boxes  # Boxes object for bbox outputs

                    class_ids = boxes.cls.cpu().numpy().astype(int)  # 转为int类型数组
                    unique_classes, counts = np.unique(class_ids, return_counts=True)  # 获取每一类的数量

                    # 更新每个类别的累计数量
                    for cls, count in zip(unique_classes, counts):
                        if cls in total_counts:
                            total_counts[cls] += count
                        else:
                            total_counts[cls] = count

                        # 如果选择了摄像头，更新每个类别的累计时间
                        if self.use_fps_algorithm:
                            time = count / fps  # 计算每一帧的时间
                            if cls in total_times:
                                total_times[cls] += time
                            else:
                                total_times[cls] = time

                # 将字典转换为一个字符串
                total_counts_divided_str = '\n'.join(
                    f'{class_names[cls]}: {count / 30:.2f}' for cls, count in total_counts.items())

                # 如果选择了摄像头，显示每个类别的累计时间
                if self.use_fps_algorithm:
                    total_times_str = '\n'.join(
                        f'{class_names[cls]}: {time:.2f}' for cls, time in total_times.items())
                    total_times_text = f"Total Time:\n{total_times_str}"

                    # 更新Text widget的内容
                    self.total_time_text.delete('1.0', tk.END)
                    self.total_time_text.insert(tk.END, total_times_text)

                    # 每5秒保存一次total time
                    timer = threading.Timer(5, self.save_total_time, args=[total_times_str])
                    timer.start()
                else:
                    total_counts_divided_text = f"Total Time:\n{total_counts_divided_str}"

                    # 更新Text widget的内容
                    self.total_time_text.delete('1.0', tk.END)
                    self.total_time_text.insert(tk.END, total_counts_divided_text)

                    # 每5秒保存一次total time
                    timer = threading.Timer(5, self.save_total_time, args=[total_counts_divided_str])
                    timer.start()

                loop_time = getTickCount() - loop_start
                total_time = loop_time / (getTickFrequency())
                fps = int(1 / total_time)
                # 在图像左上角添加FPS文本
                fps_text = f"FPS: {fps:.2f}"
                # total_counts_text = f"Total Counts:\n{total_counts_str}"
                # total_counts_divided_text = f"Total Time:\n{total_counts_divided_str}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_thickness = 3
                text_color = (0, 0, 0)  # 黑色
                fps_text_position = (10, 60)  # 左上角位置
                # total_counts_text_position = (10, 90)  # 在FPS文本下方
                # total_counts_divided_text_position = (10, 600)  # 在Total Counts文本下方

                cv2.putText(annotated_frame, fps_text, fps_text_position, font, font_scale, text_color, font_thickness)
                # y = total_counts_text_position[1]
                # for line in total_counts_text.split('\n'):
                #     cv2.putText(annotated_frame, line, (10, y), font, font_scale, text_color, font_thickness)
                #     y += 30
                # y = total_counts_divided_text_position[1]
                # for line in total_counts_divided_text.split('\n'):
                #     cv2.putText(annotated_frame, line, (10, y), font, font_scale, text_color, font_thickness)
                #     y += 30
                # 将frame转换为tkinter可以显示的图像
                image = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                # 调整图像的大小以适应Tkinter窗口
                # image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.BILINEAR)
                image = image.resize((400, 300), Image.BILINEAR)
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            else:
                break
        self.cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
