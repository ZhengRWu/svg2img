import os
import cairosvg
from PIL import Image
import tkinter as tk
from tkinter import filedialog

import xml.etree.ElementTree as ET


def get_svg_dimensions(svg_file_path):
    try:
        # 解析SVG文件
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # 检查SVG根元素是否包含width和height属性
        svg_width = root.get('width')
        svg_height = root.get('height')

        if svg_width and svg_height:
            return {'width': svg_width, 'height': svg_height}
        else:
            # 如果没有width和height属性，则检查viewBox属性
            viewbox = root.get('viewBox')
            if viewbox:
                viewbox_values = viewbox.split()
                if len(viewbox_values) == 4:
                    return {'width': viewbox_values[2], 'height': viewbox_values[3]}

        # 如果未找到宽度和高度信息，返回None
        return None
    except Exception as e:
        print(f"获取SVG尺寸时出错: {str(e)}")
        return None


def convert_svg_to_jpeg(svg_file_path, output_quality=100, output_width=2000, output_height=2000):
    # 获取SVG文件所在目录和文件名
    svg_dir, svg_filename = os.path.split(svg_file_path)

    # 使用cairosvg将SVG文件渲染为Cairo画布，并将颜色模式设置为RGB
    cairosvg.svg2png(url=svg_file_path, write_to=os.path.join(svg_dir, "temp.png"), background_color="white",
                     output_width=output_width, output_height=output_height)

    # 打开渲染后的PNG图像并将其另存为JPEG格式
    img = Image.open(os.path.join(svg_dir, "temp.png"))
    jpeg_path = os.path.splitext(svg_file_path)[0] + ".jpg"
    img = img.convert("RGB")  # 将颜色模式转换为RGB
    img.save(jpeg_path, "JPEG", quality=output_quality)

    # 删除临时PNG文件
    os.remove(os.path.join(svg_dir, "temp.png"))


def choose_svg_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename(title="选择SVG文件", filetypes=[("SVG文件", "*.svg")])
    return file_path


# 指定SVG文件的路径
svg_file_path = choose_svg_file()

dimensions = get_svg_dimensions(svg_file_path)
output_width = 4000
# 调用函数将SVG文件转换为高质量的JPEG图像
convert_svg_to_jpeg(svg_file_path, output_quality=100, output_width=output_width,
                    output_height=int(dimensions['height']) / int(dimensions['width']) * output_width)
