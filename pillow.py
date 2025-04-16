import os
from PIL import Image

def fill_transparent_with_white(input_path, output_path):
    """
    将透明区域填充为白色
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    """
    img = Image.open(input_path)
    if img.mode in ('RGBA', 'LA'):
        # 创建白色背景
        background = Image.new(img.mode[:-1], img.size, "white")
        # 合并原图和背景
        background.paste(img, mask=img.split()[-1])  # 用透明度通道作为蒙版
        background.save(output_path, "PNG")  # 保存为PNG保持透明填充效果
    else:
        # 如果图片无透明通道，直接复制
        img.convert("RGB").save(output_path, "JPEG")

def batch_process(input_dir="input", output_dir="output"):
    """
    批量处理目录中的图片
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for i, filename in enumerate(files):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        fill_transparent_with_white(input_path, output_path)
        print(f"Processed {i+1}/{len(files)}: {filename}")

if __name__ == "__main__":
    # 使用示例（默认输入目录为 input，输出目录为 output）
    batch_process(input_dir="png_start_1_touming", output_dir="png_start_1")