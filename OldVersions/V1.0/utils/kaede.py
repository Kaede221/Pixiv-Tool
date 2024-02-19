import string
import random
import os
import json
import pandas as pd
import altair as alt
import gradio as gr


def getRandomString(length: int) -> str:
    """
    获取一段指定长度的随机字符串
    :param length: 需要的长度
    :return: 字符串
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length))


def mergeJsonFiles(progress=gr.Progress()) -> str:
    """
    合并jsons目录中的所有JSON文件（遵循K格式），保存为data.json
    :return: 一个数组，包含了新增的数量之类的东西
    """
    # 创建列表，方便统计
    # 最终的列表，统计一下
    dataListFinal = []
    # 新增的数量
    newFilesCounter = 0

    # 读取pids文件
    with open('pids.json', 'r', encoding='utf-8') as f:
        # 这个是用来统计pid的，通过pid判断是否出现过这张图片
        pidsList = json.loads(f.read())

    # 遍历文件夹
    for file in os.listdir('jsons'):
        with open(f'jsons/{file}', 'r', encoding='utf-8') as f:
            # 如果扫描到输出文件，那么跳过就好
            if file == 'data.json':
                continue
            # 获取文件中的标准数组
            arrTemp = json.loads(f.read())
            for item in progress.tqdm(arrTemp, desc="文件加载中..."):
                # 查看pid是否在列表中
                if item['pid'] not in pidsList:
                    # 不存在的话，就添加到pids里面
                    pidsList.append(item['pid'])
                    # 并且追加
                    dataListFinal.append(item)
                    # 计数+1
                    newFilesCounter += 1
        # 读取完成，删除文件即可
        os.remove(f'jsons/{file}')

    # 保存pids文件，方便下次使用
    with open('pids.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(pidsList))

    # 保存数据为另外一个文件
    with open(f'jsons/data.json', 'r', encoding='utf-8') as f:
        data: list = json.loads(f.read())
        # 开始追加数据
        for i in progress.tqdm(dataListFinal, desc='追加数据中...'):
            data.append(i)
        # 保存数据
        with open(f'jsons/data.json', 'w', encoding='utf-8') as f2:
            f2.write(json.dumps(data))

    # 返回值
    return f'完成！新增{newFilesCounter}条数据！'


def getTagPencent(TAG: str, FILE_NAME: str, progress=gr.Progress()):
    """
    获取某一个Tag的占比
    :param TAG: 需要查询的Tag（具体名称）
    :param FILE_NAME: 查询的文件
    :param progress: gradio自带的进度条
    :return: 一个饼图
    """
    try:
        # 读取目标文件
        with open(f"jsons/{FILE_NAME}", "r", encoding="utf-8") as f:
            # 这个f里面默认是一个大的数组
            arr_tmp = json.loads(f.read())
            # 定义两个临时变量，r18与否
            is_r18 = 0
            total = 0
            # 遍历这个文件
            for ITEM in progress.tqdm(arr_tmp, "计算中"):
                if TAG in ITEM["tags"]:
                    is_r18 += 1
                total += 1
            # 返回数据
            result = [is_r18, total - is_r18]
            data = [result[0], result[1]]
            # 创建数据
            source = pd.DataFrame({
                "category": [f"{TAG}: {result[0]}", f"非{TAG}: {result[1]}"],
                "value":
                    data
            })
            # 创建表格并且返回
            return alt.Chart(source).mark_arc().encode(theta="value",
                                                       color="category")
    except:
        return


def getTagsRank(file: str, times: int, progress=gr.Progress()):
    """
    获取某一个tag的占比
    :param file: 查询的文件
    :param times: 查询的前n个
    :param progress: 默认进度条
    :return: 一个alt图表
    """
    times = int(times)
    try:
        with open(f"jsons/{file}", "r", encoding="utf-8") as f:
            # 获取所有的data文件
            data = json.loads(f.read())
            # 创建字典，key-value = Tag-出现次数
            tags_dict = {}
            # 开始遍历这个文件
            for item in progress.tqdm(data, "获取中..."):
                # 获取这个item的tags列表，直接遍历
                for tag in item['tags']:
                    # 判断字典是否存储了这个tag
                    if tag in tags_dict:
                        # 在的话直接加一就好
                        tags_dict[tag] += 1
                    else:
                        # 不存在，直接初始化这个键值对
                        tags_dict[tag] = 1
            # 获取完毕，进行排序，从高到低进行排序就好，获取一个列表
            final_list = sorted(tags_dict.items(),
                                key=lambda kv: (kv[1], kv[0]),
                                reverse=True)[:times]
            # 初始化两个新的变量，用来存储tag名和对应数据
            tags_list = []
            count_list = []
            # 遍历数据列表
            for item in final_list:
                tags_list.append(item[0])
                count_list.append(item[1])
            # 创建数据
            source = pd.DataFrame({
                # 设定分类
                "Tags": tags_list,
                "数量": count_list
            })

            # 创建图标
            return alt.Chart(source).mark_bar().encode(y="Tags", x="数量")
    except:
        print("文件不存在或路径错误")
