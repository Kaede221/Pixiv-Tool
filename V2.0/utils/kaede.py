import string
import random
import os
import json
from utils.pixiv import Pixiv
from tqdm import tqdm


def getRandomString(length: int) -> str:
    """
    获取一段指定长度的随机字符串
    :param length: 需要的长度
    :return: 字符串
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def mergeJsonFiles() -> str:
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
    with open("pids.json", "r", encoding="utf-8") as f:
        # 这个是用来统计pid的，通过pid判断是否出现过这张图片
        pidsList = json.loads(f.read())

    # 遍历文件夹
    for file in os.listdir("jsons"):
        with open(f"jsons/{file}", "r", encoding="utf-8") as f:
            # 如果扫描到输出文件，那么跳过就好
            if file == "data.json":
                continue
            # 获取文件中的标准数组
            arrTemp = json.loads(f.read())
            for item in tqdm(arrTemp, desc="加载中！"):
                # 查看pid是否在列表中
                if item["pid"] not in pidsList:
                    # 不存在的话，就添加到pids里面
                    pidsList.append(item["pid"])
                    # 并且追加
                    dataListFinal.append(item)
                    # 计数+1
                    newFilesCounter += 1
        # 读取完成，删除文件即可
        os.remove(f"jsons/{file}")

    # 保存pids文件，方便下次使用
    with open("pids.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(pidsList))

    # 保存数据为另外一个文件
    with open(f"jsons/data.json", "r", encoding="utf-8") as f:
        data: list = json.loads(f.read())
        # 开始追加数据
        for i in tqdm(dataListFinal, desc="追加数据中"):
            data.append(i)
        # 保存数据
        with open(f"jsons/data.json", "w", encoding="utf-8") as f2:
            f2.write(json.dumps(data))

    # 返回值
    print(f"完成！新增{newFilesCounter}条数据！")


def Init() -> Pixiv:
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
    # 读取配置文件
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
        # 顺便直接返回一个实例化对象就好
        return Pixiv(config['user']['cookie'], config['user']['user-agent'])
