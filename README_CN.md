### How to install
1. 推荐使用anaconda创建虚拟环境，conda环境配置如下：
```bash
conda create -n yolov8GUI python=3.8
```
```bash
conda activate yolov8GUI
```
2. 创建一个新的文件夹，在终端中打开并进入这个文件夹
3. 确保你已经安装了git
```bash
git --version
```
如果显示未安装，可在 [here](https://git-scm.com/downloads)下载

5. 克隆项目仓库
```bash
git clone https://github.com/sxsx-G/GUI-for-yolov8-model.git
```
6. 安装必要环境
```bash
pip install opencv-python
```
```bash
pip3 install ultralytics
```
7. 启动程序
```bash
cd GUI-for-yolov8-model
```
```bash
python3 plot.py
```
### 注意
1.该程序仅适用于yolov8模型
2.当您首次运行该程序时，它将在同一文件夹中创建一个名为“cache.txt”的缓存文件
3.设备：cuda（仅限Windows）、cpu（所有平台）、mps（仅限macOS）
4.程序的输出将作为txt文件保存在同一文件夹中
