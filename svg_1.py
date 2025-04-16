import xml.etree.ElementTree as ET
import os

input_dir = "svgs"
output_dir = "svg_1"

def simplify_svg(input_path, output_path):
    # 注册命名空间（防止自动添加 ns0）
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    
    # 解析输入文件
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    # 创建新 SVG 根元素（保留原属性）
    new_root = ET.Element("svg", attrib={
        "version": root.attrib.get("version", "1.1"),
        "viewBox": root.attrib.get("viewBox", "0 0 1024 1024"),
        "xmlns": "http://www.w3.org/2000/svg"
    })
    
    # 查找目标 <g> 元素（包含 scale(1, -1) translate(0, -900)）
    target_group = None
    for g in root.findall(".//{http://www.w3.org/2000/svg}g"):
        transform = g.attrib.get("transform", "")
        if "scale(1, -1)" in transform and "translate(0, -900)" in transform:
            target_group = g
            break
    
    if target_group is not None:
        # 复制该 <g> 元素并清理子元素
        new_group = ET.SubElement(new_root, "g", attrib=target_group.attrib)
        
        # 仅保留 fill="lightgray" 的 <path> 并修改颜色
        for elem in target_group:
            if elem.tag.endswith("path") and elem.attrib.get("fill") == "lightgray":
                # 创建新路径并修改填充色
                new_path = ET.SubElement(
                    new_group,
                    "path",
                    attrib={k: v for k, v in elem.attrib.items() if k != "id"}
                )
                new_path.set("fill", "black")
    
    # 写入输出文件
    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_path, encoding="utf-8", xml_declaration=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".svg"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        simplify_svg(input_path, output_path)