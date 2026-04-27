import cv2
import numpy as np
import os

# ========== 配置 ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, '实验视频', '实物', 'S', 'S实验视频.mp4')  # 视频路径
OUTPUT_IMAGE = os.path.join(BASE_DIR, 'output_redraw_results', 'vedio', 'ghost_result.png')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_redraw_results', 'vedio', 'screenshots')  # 截图输出目录
# 指定采样时间点（秒）
# SAMPLE_TIMES = [8.5, 18.5, 45, 57, 74, 92.5, 111.5, 129.5, 152, 166.5, 185, 200]  # 仿真
# SAMPLE_TIMES = [0.0, 12.7, 27.0, 35]  # 实物直线
# SAMPLE_TIMES = [0.0, 12.0, 27.0, 42.0, 55.0, 68.0]  # 实物S型
SAMPLE_TIMES = [0.0, 10.0, 30.0, 45.0, 70.0]  # 实物S型


MODE = 'screenshot'  # 'ghost' (鬼影图)、'darker'、'lighter'、'screenshot' (截图模式)
GHOST_METHOD = 'darker'  # ghost模式下的融合方式: 'darker' 或 'lighter'
# ==========================

def create_ghost_image():
    if 'SAMPLE_TIMES' not in globals() or not SAMPLE_TIMES:
        print("请先配置 SAMPLE_TIMES（单位：秒）")
        return

    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)

    # 尝试不同的OpenCV后端避免GStreamer问题
    cap = cv2.VideoCapture(VIDEO_PATH, cv2.CAP_FFMPEG)
    
    if not cap.isOpened():
        print(f"使用FFMPEG后端无法打开视频，尝试默认后端...")
        cap = cv2.VideoCapture(VIDEO_PATH)
        
    if not cap.isOpened():
        print(f"无法打开视频文件: {VIDEO_PATH}")
        print("请检查文件是否存在且格式正确")
        return

    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"视频信息: FPS={fps:.2f}, 总帧数={total_frames}, 时长={duration:.2f}秒")
    
    # 将采样时间点转换为帧号
    sample_frames = [int(t * fps) for t in SAMPLE_TIMES]
    print(f"采样时间点: {SAMPLE_TIMES}")
    print(f"对应帧号: {sample_frames}")
    
    # 截图模式：保存每个时间点的截图
    if MODE == 'screenshot':
        # 创建输出目录
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"\n截图模式：将保存 {len(SAMPLE_TIMES)} 张截图到 {OUTPUT_DIR}")
        
        for sample_time, frame_num in zip(SAMPLE_TIMES, sample_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            
            if not ret:
                print(f"警告: 无法读取帧 {frame_num} (时间: {sample_time}秒)")
                continue
            
            # 生成文件名：screenshot_008.5s.png
            output_filename = os.path.join(OUTPUT_DIR, f"screenshot_{sample_time:06.1f}s.png")
            cv2.imwrite(output_filename, frame)
            print(f"已保存: {output_filename}")
        
        cap.release()
        print(f"\n完成！共保存了截图到 {OUTPUT_DIR}")
        return
    
    print("开始处理视频...")

    # 兼容旧模式 + 新增 ghost 模式
    if MODE == 'ghost':
        fuse_mode = GHOST_METHOD
    elif MODE in ('darker', 'lighter'):
        fuse_mode = MODE
    else:
        print(f"不支持的 MODE: {MODE}，请使用 'ghost'/'darker'/'lighter'/'screenshot'")
        cap.release()
        return
    
    # 读取第一个采样时间点的帧作为背景画布
    cap.set(cv2.CAP_PROP_POS_FRAMES, sample_frames[0])
    ret, background = cap.read()
    if not ret: 
        print(f"无法读取帧 {sample_frames[0]}")
        return
    print(f"Processing frame {sample_frames[0]} (时间: {SAMPLE_TIMES[0]}秒) - 初始背景")
    
    # 从第二个采样点开始遍历
    for sample_time, frame_num in zip(SAMPLE_TIMES[1:], sample_frames[1:]):
        # 跳到指定帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        
        if not ret:
            print(f"警告: 无法读取帧 {frame_num} (时间: {sample_time}秒)")
            continue
        
        print(f"Processing frame {frame_num} (时间: {sample_time}秒)")
        
        # 核心逻辑：融合
        if fuse_mode == 'darker':
            background = np.minimum(background, frame)
        else:
            background = np.maximum(background, frame)

    cap.release()
    
    # 保存结果
    cv2.imwrite(OUTPUT_IMAGE, background)
    print(f"完成！图片已保存为 {OUTPUT_IMAGE}")

if __name__ == '__main__':
    create_ghost_image()