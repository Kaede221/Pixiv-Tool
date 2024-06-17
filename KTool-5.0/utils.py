"""
工具类
可以实例化，从而调用里面的方法
"""
import json
import logging as log
import os
import random
import string
import time
from urllib.parse import quote
import requests
import urllib3
from tqdm import tqdm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def init_project(db_name: str) -> bool:
    """
    初始化项目
    会创建需要的文件夹，文件，并且检查是否存在意外的问题
    :return: 是否初始化成功
    """
    try:
        # 初始化jsons文件夹
        if not os.path.exists('jsons'):
            log.warning('jsons 文件夹不存在，已创建')
            os.mkdir('jsons')
        # 初始化data.json
        if not os.path.exists(f'jsons/{db_name}'):
            log.warning(f'{db_name} 文件不存在，已创建')
            with open(f'jsons/{db_name}', 'w', encoding='utf-8') as f:
                f.write('[]')
        # 初始化pids文件-这个文件用于加快合并数据库的速度
        if not os.path.exists(f'pids.json'):
            log.warning(f'pids.json 文件不存在，已创建')
            with open(f'pids.json', 'w', encoding='utf-8') as f:
                f.write('[]')
    except IOError:
        log.error('文件读写错误')
        return False
    finally:
        log.info('项目初始化完成！')
        return True


def get_random_string(length: int) -> str:
    """
    获取一段指定长度的随机字符串
    :param length: 需要的长度
    :return: 字符串
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length))


def merge_json_files(db_name: str) -> dict:
    """
    合并json文件
    :param progress:
    :param db_name: 不动数据库文件名称，不会被修改
    :return: 返回一个列表，包含相关的数据
    """
    # 创建列表，方便统计
    # 最终的列表，统计一下
    final_data_list = []
    # 新增的数量
    files_counter = 0

    # 读取pids文件
    with open('pids.json', 'r', encoding='utf-8') as f:
        # 这个是用来统计pid的，通过pid判断是否出现过这张图片
        pids_list = json.loads(f.read())

    # 遍历文件夹
    for file in os.listdir('jsons'):
        with open(f'jsons/{file}', 'r', encoding='utf-8') as f:
            # 如果扫描到输出文件，那么跳过就好
            if file == db_name:
                continue
            # 获取文件中的标准数组
            temp_arr = json.loads(f.read())
            for item in tqdm(temp_arr, desc="文件加载中..."):
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
    with open(f'jsons/{db_name}', 'r', encoding='utf-8') as f:
        data: list = json.loads(f.read())
        # 开始追加数据
        for i in tqdm(final_data_list, desc='追加数据中...'):
            data.append(i)
        # 保存数据
        with open(f'jsons/{db_name}', 'w', encoding='utf-8') as f2:
            f2.write(json.dumps(data))

    # 返回值
    return {'合并完成, 新增数据数目': files_counter}


class Pixiv:
    def __init__(self, cookie, user_agent):
        self.cookie = cookie
        self.userAgent = user_agent

    # 在这里实现一些和pixiv相关的操作
    def get_by_illusion(self, target_origin: str):
        """
        通过Ill来获取json数据
        :param progress:
        :param target_origin: 目标链接
        :return: 下载的情况
        """
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": self.cookie,
            "user-agent": self.userAgent,
            "referer": target_origin,
        }
        url = target_origin
        session = requests.get(url, headers=headers, verify=False)
        json_get = session.json()

        # 创建一个空列表，用来储存json
        empty_arr = []
        # 通过遍历的方式获取所有的id
        for ID in tqdm(json_get["body"], "下载中..."):
            # 创建一个临时字典和完成的字典
            temp_dict: dict = json_get["body"][ID]
            get_dict: dict = {"pid": int(ID), "p": temp_dict["pageCount"], "uid": temp_dict["userId"],
                              "title": temp_dict["title"], "author": temp_dict["userName"]}
            # r18主要是根据R-18标签进行判断，其他的这里不做考虑
            if "R-18" in temp_dict["tags"]:
                get_dict["r18"] = True
            else:
                get_dict["r18"] = False
            get_dict["width"] = temp_dict["width"]
            get_dict["height"] = temp_dict["height"]
            get_dict["tags"] = temp_dict["tags"]
            # 通过ID转换为网址
            url = "https://www.pixiv.net/ajax/illust/" + ID + "/pages?lang=zh"
            # 获取对应的图片链接
            session = requests.get(url, headers=headers, verify=False)
            new_json = session.json()
            get_dict["url"] = new_json["body"][0]["urls"]["original"]
            empty_arr.append(get_dict)
        # 导出记录完毕的json数据
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return '下载完成！'

    def get_by_tag(self, _tag: str):
        keyword = quote(_tag)
        target = f"https://www.pixiv.net/ajax/search/artworks/{keyword}?word={keyword}&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": self.cookie,
            "user-agent": self.userAgent,
            "referer": target,
        }
        session = requests.get(target, headers=headers, verify=False)
        session_json = session.json()

        permanent = session_json["body"]["popular"]["permanent"]

        # 创建一个空列表，用来储存json
        empty_arr = []

        for ITEM in tqdm(permanent, "下载Popular中"):
            try:
                # 创建字典
                empty_dict: dict = {"pid": int(ITEM["id"]), "p": ITEM["pageCount"], "uid": ITEM["userId"],
                                    "title": ITEM["title"], "author": ITEM["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in ITEM["tags"]:
                    empty_dict["r18"] = True
                else:
                    empty_dict["r18"] = False
                empty_dict["width"] = ITEM["width"]
                empty_dict["height"] = ITEM["height"]
                empty_dict["tags"] = ITEM["tags"]
                # 通过ID转换为网址
                _url = f"https://www.pixiv.net/ajax/illust/{empty_dict['pid']}/pages?lang = zh"
                # 获取对应的图片链接
                session = requests.get(_url, headers=headers, verify=False)
                _json = session.json()
                empty_dict["url"] = _json["body"][0]["urls"]["original"]
                # empty_dict["urls"] = JSON1["body"][0]["urls"]
                empty_arr.append(empty_dict)
            except:
                continue
        with open(f"jsons/POPULAR_{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))

        # 另外一个
        recent = session_json["body"]["popular"]["recent"]
        for ITEM in tqdm(recent, "下载Recent中"):
            try:
                empty_dict: dict = {"pid": int(ITEM["id"]), "p": ITEM["pageCount"], "uid": ITEM["userId"],
                                    "title": ITEM["title"], "author": ITEM["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in ITEM["tags"]:
                    empty_dict["r18"] = True
                else:
                    empty_dict["r18"] = False
                empty_dict["width"] = ITEM["width"]
                empty_dict["height"] = ITEM["height"]
                empty_dict["tags"] = ITEM["tags"]
                # 通过ID转换为网址
                _url = f"https://www.pixiv.net/ajax/illust/{empty_dict['pid']}/pages?lang = zh"
                # 获取对应的图片链接
                session = requests.get(_url, headers=headers, verify=False)
                _json = session.json()
                empty_dict["url"] = _json["body"][0]["urls"]["original"]
                empty_arr.append(empty_dict)
            except:
                # 否则直接下一个就好
                continue
        with open(f"jsons/RECENT_{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return '下载完成'

    def get_by_user(self, _target: str):
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": self.cookie,
            "user-agent": self.userAgent,
            "referer": _target,
        }
        URL = _target
        session = requests.get(URL, headers=headers, verify=False)
        JSON = session.json()

        # 创建一个空列表，用来储存json
        empty_arr = []

        for ID in tqdm(JSON["body"]["works"], "获取中"):
            # 因为随时会出现报错，所以加上一个判断，报错了直接跳过去就好~
            try:
                # 创建一个临时字典和空字典
                temp_dict: dict = JSON["body"]["works"][ID]
                empty_dict: dict = {"pid": int(ID), "p": temp_dict["pageCount"], "uid": temp_dict["userId"],
                                    "title": temp_dict["title"], "author": temp_dict["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in temp_dict["tags"]:
                    empty_dict["r18"] = True
                else:
                    empty_dict["r18"] = False
                empty_dict["width"] = temp_dict["width"]
                empty_dict["height"] = temp_dict["height"]
                empty_dict["tags"] = temp_dict["tags"]
                # 通过ID转换为网址
                URL = "https://www.pixiv.net/ajax/illust/" + ID + "/pages?lang=zh"
                # 获取对应的图片链接
                session = requests.get(URL, headers=headers, verify=False)
                JSON1 = session.json()
                empty_dict["url"] = JSON1["body"][0]["urls"]["original"]
                empty_arr.append(empty_dict)
            except ConnectionError:
                log.error('连接错误，继续运行')
                continue
        # 导出记录完毕的json数据
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return "下载完成！"

    def mode_gate(self, _mode: str, _target):
        if _target == "":
            print('你没有输入内容哦！')
            return
        if _mode == 'Ill':
            self.get_by_illusion(_target)
        if _mode == 'User':
            self.get_by_user(_target)
        if _mode == 'Tag':
            self.get_by_tag(_target)


def hum_convert(value):
    # 单位转换器
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


def stats_json(db_name: str) -> dict:
    log.info('处理中...不要着急')
    with open(f'jsons/{db_name}', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    data_size = hum_convert(os.stat(f'jsons/{db_name}').st_size)
    return {
        '数据量': len(data),
        '文件大小': data_size
    }
