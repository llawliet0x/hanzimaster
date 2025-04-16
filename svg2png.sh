#!/bin/bash

# 检查Inkscape是否安装
if ! command -v inkscape &> /dev/null
then
    echo "错误：Inkscape未安装，请先安装Inkscape"
    exit 1
fi

# 定义路径
input_dir="svg_start_1"
output_dir="png_start_1_touming"

# 创建输出目录
mkdir -p "$output_dir"

# 计数器
success=0
fail=0

# 遍历所有SVG文件
for input_file in "$input_dir"/*.svg; do
    # 获取文件名（不含路径）
    filename=$(basename -- "$input_file")
    # 生成输出路径
    output_file="$output_dir/${filename%.*}.png"

    # 执行转换命令
    if inkscape "$input_file" -o "$output_file"; then
        echo "已转换: $filename → ${filename%.*}.png"
        ((success++))
    else
        echo "转换失败: $filename"
        ((fail++))
    fi
done

# 输出统计结果
echo ""
echo "================================"
echo "转换完成！"
echo "成功: $success 个"
echo "失败: $fail 个"
echo "输出目录: $output_dir"