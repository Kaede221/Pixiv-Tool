"""
查看data文件的一些相关数据
"""
import json
import os

import gradio as gr


def convert_size(size_in_bytes):
    # 文件大小格式化
    units = ["B", "KB", "MB", "GB", "TB"]

    # 依次将文件大小除以1024，并更新单位，直到文件大小小于1024
    unit_index = 0
    while size_in_bytes >= 1024 and unit_index < len(units) - 1:
        size_in_bytes /= 1024
        unit_index += 1

    # 格式化文件大小并返回
    return f"{round(size_in_bytes, 2)} {units[unit_index]}"


class DataInfo:
    def __init__(self, database_name):
        self.database_name = database_name

    def get_file_info(self):
        """
        查看文件相关的信息, 比如文件大小, 文件中数据的数量
        :return: 查阅到的数据
        """
        with open(f'jsons/{self.database_name}', 'r', encoding='utf-8') as f:
            data_list = json.loads(f.read())

        return {
            "数据数量": len(data_list),
            "文件大小": convert_size(os.stat(f'jsons/{self.database_name}').st_size)
        }

    def get_tag_percentage(self, tag: str, progress=gr.Progress()):
        # 读取文件
        with open(f'jsons/{self.database_name}', 'r', encoding='utf-8') as f:
            data_list = json.loads(f.read())
        # 数据数量
        data_num = len(data_list)
        # 直接遍历, 查看tag是否存在与某个作品, 存在的话+1
        counter = 0
        for item in progress.tqdm(data_list, "读取中"):
            if tag in item['tags']:
                counter += 1

        return f"{tag}在总数居中占比: {str(counter / data_num)[:4] + '%'}"

    def get_tag_rank(self, num: int, progress=gr.Progress()):
        # 读取文件
        with open(f'jsons/{self.database_name}', 'r', encoding='utf-8') as f:
            data_list = json.loads(f.read())
        tags_dict = {}
        # 接下来就是双重遍历了
        for item in progress.tqdm(data_list):
            for tag in item['tags']:
                if tag in tags_dict:
                    tags_dict[tag] += 1
                else:
                    tags_dict[tag] = 1

        return sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)[:num]

    def get_gui(self):
        gr.Markdown("查看数据库信息, 比如文件大小之类的东西")
        gr.Textbox(self.database_name, label="数据库名称", max_lines=1)
        usr_output = gr.Textbox(label="结果回显", lines=3, max_lines=3, interactive=False)
        usr_file_info_btn = gr.Button("获取文件信息")

        with gr.Row():
            with gr.Column():
                usr_tag = gr.Textbox(label="目标Tag", max_lines=1)
            with gr.Column():
                usr_num = gr.Number(label="前n个标签", minimum=1, step=1, precision=0, value=5)
        usr_output2 = gr.Textbox(label="结果回显", elem_id="Hi Kai", lines=3, max_lines=3, interactive=False)
        with gr.Row():
            with gr.Column():
                usr_tag_btn1 = gr.Button("查询Tag占比")
            with gr.Column():
                usr_tag_btn2 = gr.Button("查询前n个Tag及数量")
        # 绑定事件
        usr_file_info_btn.click(self.get_file_info, outputs=usr_output)
        usr_tag_btn1.click(self.get_tag_percentage, usr_tag, usr_output2)
        usr_tag_btn2.click(self.get_tag_rank, usr_num, usr_output2)
