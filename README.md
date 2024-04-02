## A python program for visualizing YOLOv8 detecting

<img width="1192" alt="截屏2024-04-02 下午4 40 33" src="https://github.com/sxsx-G/Interface-for-yolov8-model-/assets/107988674/ca2e773d-1cf7-4927-9b6e-ed48c6838273">

### How to install
1. For easy to use, you can use the anaconda to create a new environment
```bash
conda create -n yolov8GUI python=3.8
```
```bash
conda activate yolov8GUI
```
2. New a folder and open terminal in the folder
3. Make sure you have installed git
```bash
git --version
```
if you haven't installed git, you can download it from [here](https://git-scm.com/downloads)

5. Clone the repository from github
```bash
git clone https://github.com/sxsx-G/GUI-for-yolov8-model.git
```
6. Install the required packages
```bash
pip install opencv-python
```
```bash
pip3 install ultralytics
```
7. Start the program
```bash
cd GUI-for-yolov8-model
```
```bash
python3 plot.py
```
### Notifications
1. The program is only for the yolov8 model
2. When you first run the program, it will gnerate a cache file named "cache.txt" in the same folder
3. Device: cuda(Windows only), cpu(all platform), mps(macOS only)
4. The outputs of the program will be saved as a txt file in the same folder
5. If notice any problems, please report on 'Issues'

