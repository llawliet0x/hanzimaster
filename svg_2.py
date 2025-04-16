import os
import xml.etree.ElementTree as ET

input_dir = "svg_1"
output_dir = "svg_2"

def split_svg_by_paths(input_path, output_dir):
    # 解析 XML
    tree = ET.parse(input_path)
    root = tree.getroot()

    # 命名空间处理
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    ET.register_namespace('', ns['svg'])

    # 获取原文件名（不含扩展名）
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    # 找到 <g> 标签（含 transform 的那一层）
    g_tag = root.find('svg:g', ns)
    if g_tag is None:
        print(f"没有找到 <g> 标签：{input_path}")
        return

    # 找出所有 <path> 标签
    paths = g_tag.findall('svg:path', ns)

    # 按照每个 path 拆分
    for idx, path in enumerate(paths, start=1):
        # 构建新的 SVG 根节点
        new_svg = ET.Element("svg", attrib={
        "version": root.attrib.get("version", "1.1"),
        "viewBox": root.attrib.get("viewBox", "0 0 1024 1024")
    })

        # 构建新的 <g> 标签，保留 transform
        new_g = ET.Element('g', {
            'transform': g_tag.attrib.get('transform', '')
        })

        # 添加当前 path
        new_g.append(path)

        # 组装
        new_svg.append(new_g)

        # 创建树并写入
        new_tree = ET.ElementTree(new_svg)
        output_path = os.path.join(output_dir, f"{base_name}{idx}.svg")
        new_tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"生成：{output_path}")


#split_svg_by_paths("11904.svg", ".")


for filename in os.listdir(input_dir):
    if filename.endswith(".svg"):
        input_path = os.path.join(input_dir, filename)
        split_svg_by_paths(input_path, output_dir)
# def batch_split_svgs(input_dir, output_dir):
#    os.makedirs(output_dir, exist_ok=True)
#    for file in os.listdir(input_dir):
#        if file.endswith('.svg'):
#            input_path = os.path.join(input_dir, file)
#            split_svg_by_paths(input_path, output_dir)

# if __name__ == "__main__":
#    input_directory = "svgs"
#    output_directory = "svg_1"
#    batch_split_svgs(input_directory, output_directory)
