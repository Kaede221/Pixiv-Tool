"""
本文件用于构建GUI前端页面
"""
import gradio as gr
import utils as utils


def get_gui(cookie: str, user_agent: str, db_name: str) -> gr.Blocks:
    """
    构建GUI界面，并且返回root
    :return: 一个gradio的对象
    """
    # 初始化项目
    utils.init_project(db_name)

    # 实例化pixiv
    pixiv = utils.Pixiv(cookie, user_agent)

    with gr.Blocks() as root:
        gr.Markdown('# KTool-5.0')
        gr.Markdown('集获取数据，修改数据于一体的工具箱！')
        with gr.Tab('获取'):
            with gr.Row():
                with gr.Column(scale=5):
                    gr.Markdown('## 获取数据')
                    gr.Markdown('根据规则，输入需要的内容即可')
                    # 选择获取模式
                    choose_mode = gr.Radio(['Ill', 'User', 'Tag'], value='User')
                    # 给一个输入框，允许输入url或者tag
                    input_url = gr.Textbox(label='输入目标url或者tag', max_lines=1)
                with gr.Column(scale=5):
                    gr.Markdown('## 操作')
                    start_btn = gr.Button('开始获取数据')
                    output_box = gr.Textbox(label='会在这里返回需要的内容', lines=2, max_lines=3)
            # 绑定相关按钮之类的东西
            start_btn.click(fn=pixiv.mode_gate, inputs=[choose_mode, input_url], outputs=output_box)
        with gr.Tab('处理'):
            with gr.Row():
                with gr.Column():
                    gr.Markdown('## 操作文件')
                    input_path = gr.Textbox(label='目标目录')
                    merge_button = gr.Button('开始合并文件')
                    output_box2 = gr.Textbox(label='进度回显')

    # 配置
    root.queue(max_size=6)
    return root
