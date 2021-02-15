# FFmpeg-Pipe-Python
在 Python 内直接调用 FFmpeg 来读取和写入视频

先运行 read.py，它会在项目根目录创建一个 img 文件夹，把 in_v.mp4 的每一帧保存进去。
再运行 write.py，它会把刚刚解出来 img 文件夹内的图像再编码成视频并保存为 out_v.mp4。

详细信息看代码注释
