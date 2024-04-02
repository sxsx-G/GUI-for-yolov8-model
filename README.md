## A python program for visualizing YOLOv8 detecting

![Uploading 截屏2024-04-02 下午4.40.33.png…]()

### How to install
1. For easy to use, you can use the anaconda to create a new environment
```bash
conda create -n yolov8GUI python=3.8
```
2. New a folder and open terminal in the folder
3. Make sure you have installed git
```bash
git --version
```
if you haven't installed git, you can download it from [here](https://git-scm.com/downloads)

5. Clone the repository from github
```bash
git clone https://github.com/sxsx-G/Interface-for-yolov8-model-.git
```
6. Install the required packages
```bash
pip3 install ultralytics
```
7. Start the program
```bash
python3 plot.py
```
### Notifications
1. The program is only for the yolov8 model
2. When you first run the program, it will gnerate a cache file named "cache.txt" in the same folder
3. Device: cuda(Windows only), cpu(all platform), mps(macOS only)
4. The outputs of the program will be saved as a txt file in the same folder
