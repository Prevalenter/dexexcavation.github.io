import os
import subprocess
import time

def compress_video(input_path, output_path, crf=36):
    """
    使用 FFmpeg 压缩视频
    :param input_path: 原视频路径
    :param output_path: 输出视频路径
    :param crf: 压缩质量系数 (0-51)。23是默认，28是推荐压缩值，值越大体积越小画质越差。
    """
    # 构造 FFmpeg 命令
    # -i: 输入
    # -vcodec libx264: 使用 H.264 编码 (兼容性最好)
    # -crf: 控制画质/体积的关键参数
    # -preset faster: 编码速度优先 (veryfast, faster, fast, medium, slow...)
    # -y: 覆盖已存在的输出文件
    command = [
        'ffmpeg', 
        '-y', 
        '-i', input_path,
        '-vcodec', 'libx264',
        '-crf', str(crf),
        '-preset', 'faster',
        output_path
    ]

    try:
        # 运行命令，stdout=subprocess.DEVNULL 表示不显示 FFmpeg 刷屏的日志，只显示报错
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 压缩出错: {input_path}")
        # 如果出错，打印 FFmpeg 的错误信息
        print(e.stderr.decode()) 
        return False

def batch_process(source_dir, target_dir):
    # 1. 如果目标文件夹不存在，创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"📁 已创建输出目录: {target_dir}")

    # 支持的视频格式后缀
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv')
    
    # 2. 遍历源文件夹
    files = [f for f in os.listdir(source_dir) if f.lower().endswith(video_extensions)]
    total_files = len(files)
    
    print(f"🚀 开始处理，共找到 {total_files} 个视频文件...")
    print("-" * 30)

    start_time = time.time()
    success_count = 0

    for index, filename in enumerate(files):
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(target_dir, filename)

        print(f"[{index+1}/{total_files}] 正在压缩: {filename} ...", end="", flush=True)
        
        # 执行压缩
        if compress_video(src_file, dst_file):
            # 计算压缩前后的体积大小对比
            src_size = os.path.getsize(src_file) / (1024 * 1024)
            dst_size = os.path.getsize(dst_file) / (1024 * 1024)
            print(f" ✅ 完成 ({src_size:.1f}MB -> {dst_size:.1f}MB)")
            success_count += 1
        else:
            print(" ❌ 失败")

    end_time = time.time()
    duration = end_time - start_time
    print("-" * 30)
    print(f"🎉 全部处理完毕！耗时: {duration:.1f}秒")
    print(f"成功: {success_count}，失败: {total_files - success_count}")

if __name__ == '__main__':
    # ================= 配置区域 =================
    # 请在这里修改你的文件夹路径 (Windows路径建议前面加 r，或者用双斜杠)
    INPUT_FOLDER = r"static/videos_raw"       # 你的源视频文件夹
    OUTPUT_FOLDER = r"static/videos" # 你想保存的文件夹
    # ===========================================

    batch_process(INPUT_FOLDER, OUTPUT_FOLDER)
    