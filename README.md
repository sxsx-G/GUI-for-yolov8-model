## A python program for visualizing YOLOv8 detecting

<img width="1192" alt="截屏2024-03-29 下午3 55 30" src="https://github.com/sxsx-G/Yolov8GUI/assets/107988674/ddebe663-f06a-4f07-ae58-d54249b1a9b1">

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