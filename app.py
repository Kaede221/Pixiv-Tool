import json

import gradio as gr
from scripts.utils import init_project
from scripts.pixiv import Pixiv

# 扩展
from modules.merge_json_files import MergeJsonFiles
from modules.data_info import DataInfo
from modules.data_filter import DataFilter

# 读取配置
with open("config.json", 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

# 设定一些常量
database_name = config['database_name']

# 初始化项目
init_project(database_name)

# 创建Pixiv对象
pixiv = Pixiv(config['user']['cookie'], config['user']['user_agent'])

# 构建UI
with gr.Blocks(theme=gr.themes.Soft()) as root:
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("# 获取数据")
            usr_mode = gr.Radio(['Ill', "User"], label="获取模式", value='User')
            usr_url = gr.Textbox(label="目标网址", placeholder="可以输入对应的链接", max_lines=1)
            usr_btn = gr.Button("开始获取")
            usr_output = gr.Textbox(label="结果回显", max_lines=3, lines=3)
            # 添加事件
            usr_btn.click(pixiv.mode_gate, [usr_mode, usr_url], usr_output)
        with gr.Column(scale=7):
            gr.Markdown("# 扩展")
            # 目前还没想出来如何自动读取扩展, 但是这就是一个小项目, 绝对够用了
            with gr.Tab("合并文件"):
                MergeJsonFiles(database_name).get_gui()
            with gr.Tab("查看数据库信息"):
                DataInfo(database_name).get_gui()
            with gr.Tab("数据清洗"):
                DataFilter(database_name).get_gui()
if __name__ == "__main__":
    root.queue(1).launch()
