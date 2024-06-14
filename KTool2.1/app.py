import gradio as gr
import yaml
import utils as utils

# 读取配置文件
with open('config.yaml', 'r', encoding='UTF-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# 初始化项目
utils.init_project(config['db_name'])
# 实例化Pixiv
pixiv = utils.Pixiv(config['cookie'], config['user_agent'])


# 函数，用于区分
def mode_gate(mode: str, _target: str):
    match mode:
        case "Ill":
            pixiv.get_by_illusion(_target)
        case "User":
            pixiv.get_by_user(_target)
        case "Tag":
            pixiv.get_by_tag(_target)


with gr.Blocks() as root:
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown('## 文件操作')
            gr.Markdown('可以在这里合并文件')
            inbox = gr.Textbox(value=config['db_name'], label='目标数据库名称', max_lines=1)
            merge_button = gr.Button('合并文件')
            outbox = gr.Textbox(label='进度', lines=3, max_lines=3)
        with gr.Column(scale=7):
            gr.Markdown("## 数据获取")
            gr.Markdown('你可以在这里下载需要的内容')
            choose_mode = gr.Radio(['Ill', 'User', 'Tag'], value='User', label='选择获取模式')
            target_url = gr.TextArea(label='输入目标链接或者Tag', lines=1, max_lines=1)
            get_btn = gr.Button('开始获取')
            outbox2 = gr.Textbox(label='进度', lines=3, max_lines=3)

    merge_button.click(fn=utils.merge_json_files, inputs=inbox, outputs=outbox)
    get_btn.click(fn=mode_gate, inputs=[choose_mode, target_url], outputs=outbox2)

if __name__ == '__main__':
    root.launch(server_port=config['port'], max_threads=5)
    pass
