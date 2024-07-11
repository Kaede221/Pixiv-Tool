"""
合并文件的扩展项目
"""
import gradio as gr
import json
import os


class MergeJsonFiles:
    def __init__(self, database_name):
        self.database_name = database_name

    def merge_json_files(self, progress=gr.Progress()) -> str:
        # 创建列表，方便统计
        # 最终的列表，统计一下
        final_data_list = []
        # 新增的数量
        files_counter = 0

        # 读取pids文件 不建议修改
        with open('pids.json', 'r', encoding='utf-8') as f:
            # 这个是用来统计pid的，通过pid判断是否出现过这张图片
            pids_list = json.loads(f.read())

        # 遍历文件夹
        for file in os.listdir('jsons'):
            with open(f'jsons/{file}', 'r', encoding='utf-8') as f:
                # 如果扫描到输出文件，那么跳过就好
                if file == self.database_name:
                    continue
                # 获取文件中的标准数组
                temp_arr = json.loads(f.read())
                for item in progress.tqdm(temp_arr, desc="文件加载中..."):
                    # 查看pid是否在列表中
                    if item['pid'] not in pids_list:
                        # 不存在的话，就添加到pids里面
                        pids_list.append(item['pid'])
                        # 并且追加
                        final_data_list.append(item)
                        # 计数+1
                        files_counter += 1
            # 读取完成，删除文件即可
            os.remove(f'jsons/{file}')

        # 保存pids文件，方便下次使用
        with open('pids.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(pids_list))

        # 保存数据为另外一个文件
        with open(f'jsons/{self.database_name}', 'r', encoding='utf-8') as f:
            data: list = json.loads(f.read())
            # 开始追加数据
            for i in progress.tqdm(final_data_list, desc='追加数据中...'):
                data.append(i)
            # 保存数据
            with open(f'jsons/{self.database_name}', 'w', encoding='utf-8') as f2:
                f2.write(json.dumps(data))
        return f'追加完成！新增{files_counter}'

    def get_gui(self):
        gr.Markdown("你可以在获取文件后, 在这里将获取的文件合并, 最后保存为一个单独的文件")
        gr.Textbox(self.database_name, interactive=False, label="数据库名称", max_lines=1)
        edit_btn = gr.Button("合并")
        edit_output = gr.Textbox(label="结果回显", max_lines=3, lines=3)
        # 添加事件
        edit_btn.click(self.merge_json_files, outputs=edit_output)
