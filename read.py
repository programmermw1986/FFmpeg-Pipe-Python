import os
import subprocess as sp
import numpy as np
import cv2

cap = cv2.VideoCapture('in_v.mov')
width, height = map(lambda x: int(cap.get(x)), (3, 4))

# videoIO
command = [
    'ffmpeg',
    '-i', 'in_v.mov',
    '-f', 'rawvideo',  # 输出numpy可读取的rawvideo
    '-s', '%dx%d' % (width, height),  # 指定宽高
    '-pix_fmt', 'bgr24',  # 输出一般cv2的像素格式
    '-'  # 输出到管道
]
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)

count = 0

os.makedirs('img', exist_ok=True)
while True:
    raw_image = pipe.stdout.read(width * height * 3)  # 从管道里读取一帧，字节数为(宽*高*3)有三个通道
    image = np.frombuffer(raw_image, dtype='uint8')  # 把读取到的二进制数据转换成numpy数组
    if len(image) == 0:  # 如果全部读取完了就结束循环
        break
    image = image.reshape((height, width, 3))  # 把图像转变成应有形状
    cv2.imwrite(f'img/{count}.jpg', image)  # 用 cv2保存图像
    pipe.stdout.flush()  # 充管道
    count += 1
# 关闭管道（关闭后FFmpeg会把缓存里的数据释放到视频文件，python脚本结束运行会自动关闭，但管道一直开着，占用系统资源）
pipe.terminate()
