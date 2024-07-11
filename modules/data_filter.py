"""
因为有些时候, 图片数据会过期(就是被作者删掉)
所以有了这个扩展, 主要就是用于排除失效的数据, 或者按照一定格式处理一遍数据
"""
import json
import gradio as gr
import requests


class DataFilter:
    def __init__(self, database_name):
        self.database_name = database_name

    def delete_pid_data(self, pid_list: str, progress=gr.Progress()):
        """
        按照pid删除数据
        :param pid_list: 传入的是一个字符串, 使用 , 分隔的数字
        :param progress: 进度条
        :return: 无
        """
        # 先判断是否为空
        if len(pid_list) == 0:
            gr.Error("请填入PID")
            return "请填入PID"
        # pid list进行转换
        pid_list = pid_list.split(",")
        # 遍历一下, 删除空格
        for i in range(len(pid_list)):
            pid_list[i] = pid_list[i].strip()

        # 读取数据
        with open(f'jsons/{self.database_name}', 'r', encoding='utf-8') as f:
            data_list: list = json.loads(f.read())

        # 这里允许同时删除多个pid, 提升效率
        for pid in pid_list:
            for item in progress.tqdm(data_list, f'检索 {pid} 中'):
                # 找pid就好
                if int(item['pid']) == int(pid):
                    # 是的话直接删掉这个数据就好, 同时退出本轮循环
                    data_list.remove(item)
                    break

        # 处理完毕, 直接覆盖源文件即可
        with open(f'jsons/{self.database_name}', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data_list))
        return "操作完成(或者pid不存在)"

    def get_gui(self):
        gr.Markdown("你可以在这里清洗数据, 从而让数据库符合自己的要求 (不过多半用于除去失效的内容)")
        gr.Textbox(self.database_name, label='数据库名称', lines=1, max_lines=1, interactive=False)
        usr_pid_target = gr.Textbox(label="PID 你可以使用英文逗号进行分割多个PID")
        usr_output = gr.Textbox(label="处理结果", lines=3, max_lines=3, interactive=False)
        usr_btn = gr.Button('删除指定PID的数据', variant="primary")

        # 添加按钮
        usr_btn.click(self.delete_pid_data, usr_pid_target, outputs=usr_output)
