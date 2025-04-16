import os
import tempfile
from PIL import Image
import subprocess

# 设置图片目录
input_dir = "./png_start_1"  # 可以修改为你的图片目录
output_dir = "./py_potrace_results"
os.makedirs(output_dir, exist_ok=True)

# 遍历 .png 文件
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".png"):
        base_name = os.path.splitext(filename)[0]
        png_path = os.path.join(input_dir, filename)
        svg_path = os.path.join(output_dir, f"{base_name}.svg")

        # 打开 PNG 图片并转为灰度图
        with Image.open(png_path) as img:
            img = img.convert("L")

            # 创建临时 BMP 文件
            with tempfile.NamedTemporaryFile(suffix=".bmp", delete=True) as tmp_bmp:
                img.save(tmp_bmp.name)

                # 用 potrace 生成 SVG
                try:
                    subprocess.run(["potrace", "-b", "svg", "--width", "1024", "--height", "1024", "-o", svg_path, tmp_bmp.name], check=True)
                    print(f"✅ 已生成 SVG：{svg_path}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ potrace 转换失败：{e}")
