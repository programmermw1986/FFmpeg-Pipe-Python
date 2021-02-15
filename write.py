import os
import subprocess as sp
import cv2

# 加载所有图片路径
files = os.listdir('img')
files = [f'img/{_}' for _ in files if _[-3:] == 'jpg']
files.sort()

# 获取图像宽高
height, width = cv2.imread(files[0]).shape[0:2]

# FFmpeg 管道
command = [
    'ffmpeg',
    '-y',  # （可选）覆盖输出文件（如果存在）
    '-f', 'rawvideo',  # rawvideo 为完整帧数据，即numpy.ndarray.tobytes()的数据
    '-s', '%dx%d' % (width, height),  # 一帧的大小
    '-pix_fmt', 'bgr24',  # cv2 返回的像素格式
    '-r', '2',  # 每秒帧数
    '-i', '-',  # 输入来自管道
    '-c:v', 'libx264',  # 用x264编码
    '-pix_fmt', 'yuv420p',  # 采用常用像素格式yuv420p
    'out_v.mp4'
]
pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

for f in files:
    img = cv2.imread(f)  # 读取图像
    pipe.stdin.write(img.tobytes())  # 把图像送到管道里给FFmpeg编码
# 关闭管道（关闭后FFmpeg会把缓存里的数据释放到视频文件，python脚本结束运行会自动关闭，但管道一直开着，占用系统资源）
pipe.terminate()
