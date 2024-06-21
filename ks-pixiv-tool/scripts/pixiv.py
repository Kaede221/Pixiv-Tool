import json
import time

import requests
from rich import print
from tqdm import tqdm


def get_image_url(url: str, headers: dict) -> str:
    """
    获取图片链接
    :param url: 最初的url，比如https://www.pixiv.net/ajax/illust/{pid}/pages
    :param headers: 一个标准的headers字典
    :return: 修改后的链接，就是直链链接
    """
    new_json = requests.get(url, headers=headers, verify=False).json()
    return new_json["body"][0]["urls"]["original"]


def get_operated_data(json_data: dict, pid: str, headers: dict) -> dict:
    """
    获取操作后的data数据
    :param json_data: 初始获得的json数据，是一个单独的对象
    :param pid: 图片的pid
    :param headers: 构造的headers
    :return: 操作完成的数据对象
    """
    # 创建一个临时字典和完成的字典
    temp_dict: dict = json_data["body"]['works'][pid]
    # 通过ID转换为网址
    url = f"https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh"
    # 操作
    return {
        "pid": int(pid),
        "p": temp_dict["pageCount"],
        "uid": temp_dict["userId"],
        "title": temp_dict["title"],
        'r18': True if ("R-18" in temp_dict["tags"]) else False,
        "author": temp_dict["userName"],
        'width': temp_dict["width"],
        'height': temp_dict["height"],
        'tags': temp_dict["tags"],
        'url': get_image_url(url, headers)
    }


class Pixiv:
    """
    Pixiv工具类，用于获取数据
    * Ill获取
    * User获取
    """

    def __init__(self, cookie, user_agent):
        self.cookie = cookie
        self.userAgent = user_agent

    def get_header(self, target_url: str) -> dict:
        """
        根据传入的目标链接，创建一个Header出来，并且返回
        :param target_url:
        :return:
        """
        return {
            "cookie": self.cookie,
            "user-agent": self.userAgent,
            "referer": target_url,
        }

    def get_by_illusion(self, target_url: str):
        """
        通过Ill来获取json数据
        :param target_url: 目标链接
        :return: 下载的情况
        """
        # 初始化
        headers = self.get_header(target_url)
        json_get = requests.get(target_url, headers=headers, verify=False).json()

        # 创建一个空列表，用来储存json
        empty_arr = []
        # 获取数据
        for ID in tqdm(json_get["body"], "下载中..."):
            empty_arr.append(get_operated_data(json_get, ID, headers))

        # 导出记录完毕的json数据
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return '下载完成！'

    def get_by_user(self, target_url: str):
        headers = self.get_header(target_url)
        json_data = requests.get(target_url, headers=headers, verify=False).json()
        # 创建一个空列表，用来储存json
        empty_arr = []
        for ID in tqdm(json_data["body"]["works"], "获取中"):
            # 因为随时会出现报错，所以加上一个判断，报错了直接跳过去就好~
            try:
                empty_arr.append(get_operated_data(json_data, ID, headers))
            except ConnectionError:
                print('连接错误')
                continue
        # 导出记录完毕的json数据
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return "下载完成！"

    def mode_gate(self, mode: str, target_url: str):
        match mode:
            case 'User':
                self.get_by_user(target_url)
            case 'Ill':
                self.get_by_illusion(target_url)
            case _:
                print('没有这个选项')
