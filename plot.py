import cv2
from ultralytics import YOLO
from cv2 import getTickCount, getTickFrequency
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading


# 加载 YOLOv8 模型
model = YOLO("/Users/herry/Downloads/best.pt")

def select_source():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    msg_box = messagebox.askquestion('选择视频源', 'yes：选择摄像头 no:选择视频', icon='warning')
    if msg_box == 'yes':
        cap = cv2.VideoCapture(0)
    else:
        video_file_path = filedialog.askopenfilename()
        if video_file_path:
            cap = cv2.VideoCapture(video_file_path)
        else:
            print("未选择文件，程序退出")
            exit(0)

    root.destroy()  # 销毁窗口

    return cap

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv8 Class Detection")
        self.root.geometry('800x600')

        # 创建按钮框架，并放置在窗口顶部
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="top", fill="x")

        self.model_button = tk.Button(self.button_frame, text="选择模型", command=self.select_model)
        self.model_button.pack(side="left")

        self.start_button = tk.Button(self.button_frame, text="选择视频源", command=self.start, state="disabled")
        self.start_button.pack(side="left")

        self.quit_button = tk.Button(self.button_frame, text="退出检测", command=self.quit, state="disabled")
        self.quit_button.pack(side="left")

        # 使用PanedWindow来改善布局
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.paned_window, height=450)  # 设置初始高度
        self.paned_window.add(self.image_frame, weight=1)  # 图像框架应该占用大部分空间

        self.total_time_frame = tk.Frame(self.paned_window, height=150)
        self.total_time_text = tk.Text(self.total_time_frame)
        self.total_time_text.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.total_time_frame, weight=0)  # 总时间框架占用较少空间

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

    def select_model(self):
        model_file_path = filedialog.askopenfilename()
        if model_file_path:
            self.model = YOLO(model_file_path)
            self.start_button.config(state="normal")
        else:
            print("未选择模型文件，程序退出")
            exit(0)

    def quit(self):
        # 关闭程序
        self.root.destroy()

    def start(self):
        self.cap = select_source()
        # 获取视频的宽度和高度
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # 设置图像Frame的大小
        self.image_frame.config(width=int(width), height=int(height))
        self.start_button.config(state="disabled")
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
            4: "using_Laptap",
            5: "writing",
            6: "talking",
            7: "sleeping",
            8: "eating"
        }

        # 创建一个字典来存储每个类别的累计数量
        total_counts = {}

        while self.cap.isOpened():
            loop_start = getTickCount()
            success, frame = self.cap.read()  # 读取摄像头的一帧图像

            if success:
                results = model.predict(source=frame) # 对当前帧进行目标检测并显示结果
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

                # 将字典转换为一个字符串
                total_counts_str = '\n'.join(f'{class_names[cls]}: {count}' for cls, count in total_counts.items())
                total_counts_divided_str = '\n'.join(f'{class_names[cls]}: {count/30:.2f}' for cls, count in total_counts.items())
                total_counts_divided_text = f"Total Time:\n{total_counts_divided_str}"

                # 更新Text widget的内容
                self.total_time_text.delete('1.0', tk.END)
                self.total_time_text.insert(tk.END, total_counts_divided_text)

                # 中间放自己的显示程序
                loop_time = getTickCount() - loop_start
                total_time = loop_time / (getTickFrequency())
                FPS = int(1 / total_time)
                # 在图像左上角添加FPS文本
                fps_text = f"FPS: {FPS:.2f}"
                total_counts_text = f"Total Counts:\n{total_counts_str}"
                total_counts_divided_text = f"Total Time:\n{total_counts_divided_str}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                font_thickness = 3
                text_color = (0, 0, 0)  # 黑色
                fps_text_position = (10, 60)  # 左上角位置
                total_counts_text_position = (10, 90)  # 在FPS文本下方
                total_counts_divided_text_position = (10, 600)  # 在Total Counts文本下方

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
                image = image.resize((self.root.winfo_width(), self.root.winfo_height()), Image.BILINEAR)
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