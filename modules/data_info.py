"""
查看data文件的一些相关数据
"""
import json

import gradio as gr


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
            "数据量: ": len(data_list)
        }

    def get_gui(self):
        gr.Markdown("查看数据库信息, 比如文件大小之类的东西")
        gr.Textbox(self.database_name, label="数据库名称", max_lines=1)
        gr.Button("获取文件信息")
