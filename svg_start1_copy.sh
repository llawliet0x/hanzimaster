#!/bin/bash

# 设置源目录和目标目录
SRC_DIR="svg_2"
DEST_DIR="svg_start_1"

# 如果目标目录不存在就创建它
mkdir -p "$DEST_DIR"

# 复制所有以1开头的svg文件
cp "$SRC_DIR"/1*.svg "$DEST_DIR"
