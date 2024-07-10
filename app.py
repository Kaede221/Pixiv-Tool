import json

import gradio as gr
from scripts.utils import init_project, merge_json_files
from scripts.pixiv import Pixiv

# 读取配置
with open("config.json", 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

# 初始化项目
init_project(config['database_name'])

# 创建Pixiv对象
pixiv = Pixiv(config['user']['cookie'], config['user']['user_agent'])

# 构建UI
with gr.Blocks(theme=gr.themes.Base()) as root:
    with gr.Row():
        with gr.Column(scale=5):
            gr.Markdown("# 获取数据")
            usr_mode = gr.Radio(['Ill', "User"], label="获取模式", value='User')
            usr_url = gr.Textbox(label="目标网址", placeholder="可以输入对应的链接", max_lines=1)
            usr_btn = gr.Button("开始获取")
            usr_output = gr.Textbox(label="结果回显", max_lines=3, lines=3)
            # 添加事件
            usr_btn.click(pixiv.mode_gate, [usr_mode, usr_url], usr_output)
        with gr.Column(scale=5):
            gr.Markdown("# 处理数据")
            edit_btn = gr.Button("合并文件")
            edit_name = gr.Textbox(config['database_name'], interactive=False, label="数据库名称")
            edit_output = gr.Textbox(label="结果回显", max_lines=3, lines=3)
            # 添加事件
            edit_btn.click(merge_json_files, edit_name, edit_output)

    if __name__ == "__main__":
        root.queue(1).launch()
