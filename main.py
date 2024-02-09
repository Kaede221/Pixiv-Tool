import yaml
import os
import gradio as gr
from utils import pixiv, kaede

# 检查是否存在jsons文件夹
if not os.path.exists('jsons'):
    print(f"文件夹不存在，已自动创建：jsons")
    os.makedirs('jsons')

# 判断是否存在pids文件
if not os.path.exists("pids.json"):
    print(f"文件不存在，已自动创建：pids.json")
    with open("pids.json", "w", encoding="utf-8") as f:
        f.write("[]")

# 判断是否存在输出文件名称
if not os.path.exists("jsons/data.json"):
    print(f"文件不存在，已自动创建：data.json")
    with open("jsons/data.json", "w", encoding="utf-8") as f:
        f.write("[]")

# 读取配置文件
with open('./config.yml', 'r', encoding='utf-8') as f:
    configData = yaml.load(f, Loader=yaml.FullLoader)

# 实例化Pixiv工具类
Pixiv = pixiv.Pixiv(configData['user']['cookie'],
                    configData['user']['user-agent'])

# 创建标准页面
with gr.Blocks() as ROOT:
    with gr.Tab("爬取Pixiv的JSON数据"):
        gr.Markdown("# Pixiv Get 2.0")
        gr.Markdown("方便的获取Pixiv的图片数据~")
        with gr.Tab("前置设定"):
            gr.Markdown("自动读取目录下的`options`文件，如果需要修改请直接修改文件")
            COOKIE = gr.Textbox(label="用户的Cookie",
                                value=configData['user']['cookie'])
            USER_AGENT = gr.Textbox(label="用户的User Agent",
                                    value=configData['user']['user-agent'])
        with gr.Tab("By Illusts"):
            TARGET = gr.Textbox(label="输入作品页面获取的json地址")
            PROGRESS = gr.TextArea(label="下载结果以及进度", lines=3)
            gr.Button("下载").click(Pixiv.getByIllusts,
                                  [TARGET, COOKIE, USER_AGENT], PROGRESS)
        with gr.Tab("By Tag"):
            TAG = gr.Textbox(label="输入Tag进行提取，不建议输入多个tag")
            PROGRESS1 = gr.TextArea(label="下载进度", lines=3)
            gr.Button("下载").click(Pixiv.getByTag,
                                  [TAG, COOKIE, USER_AGENT], PROGRESS1)

        with gr.Tab("By User"):
            URL = gr.Textbox(label="输入User页面找到的链接")
            PROGRESS2 = gr.TextArea(label="下载进度", lines=3)
            gr.Button("下载").click(Pixiv.getByUser,
                                  [URL, COOKIE, USER_AGENT], PROGRESS2)

        with gr.Tab("合并文件"):
            PROGRESS3 = gr.TextArea(label="合并进度", lines=3)
            gr.Button("开始合并文件").click(kaede.mergeJsonFiles, outputs=PROGRESS3)

        with gr.Tab("获取某一Tag占比"):
            with gr.Row():
                with gr.Column(scale=1):
                    TAG_TMP = gr.Textbox(label="检索的Tag(请保证拼写正确)")
                    FILENAME = gr.Textbox(label="检索的文件名称", value="data.json")
                    PROGRESS4 = gr.Plot(label="占比数据饼图")
                    gr.Button("开始获取占比").click(kaede.getTagPencent,
                                              [TAG_TMP, FILENAME], PROGRESS4)
                with gr.Column(scale=1):
                    # 给一些案例
                    gr.Examples(
                        [["R-18", "data.json"], ["Arknights", "data.json"],
                         ["ぱんつ", "data.json"], ["制服", "data.json"],
                         ["女の子", "data.json"], ["セーラー服", "data.json"]],
                        [TAG_TMP, FILENAME],
                        PROGRESS4,
                        kaede.getTagPencent,
                        run_on_click=True)
        with gr.Tab("获取Tags排名"):
            FILE_NAME = gr.Textbox(label="检索文件名", value="data.json", lines=1)
            COUNT = gr.Number(label="前多少个，不建议设置太多，请输入整数")
            PROGRESS5 = gr.Plot(label="排名数据")
            gr.Button("开始获取排名").click(kaede.getTagsRank,
                                      [FILE_NAME, COUNT], PROGRESS5)
    with gr.Tab("关于"):
        gr.Markdown("# Pixiv 工具集\nKaede的制作的开源软件，主要是和pixiv有关的操作~\n那么希望你玩得高兴~")
# 启动
ROOT.queue(20).launch(server_port=configData['app']['port'])
