import requests
import json
import time
import gradio as gr
from urllib.parse import quote


class Pixiv:
    def __init__(self, cookie, userAgent):
        self.cookie = cookie
        self.userAgent = userAgent

    # 在这里实现一些和pixiv相关的操作
    def getByIllusts(self, TARGET: str,
                     COOKIE: str,
                     USER_AGENT: str,
                     progress=gr.Progress()):
        """
        通过illusts来获取json数据
        :param TARGET: 目标链接，就是illusts的那个链接
        :param COOKIE: 用户的cookie
        :param USER_AGENT: 用户的agent
        :param progress: 默认进度条
        :return: 下载的情况
        """
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": COOKIE,
            "user-agent": USER_AGENT,
            "referer": TARGET,
        }
        url = TARGET
        session = requests.get(url, headers=headers, verify=False)
        json_get = session.json()

        # 创建一个空列表，用来储存json
        empty_arr = []
        # 通过遍历的方式获取所有的id
        for ID in progress.tqdm(json_get["body"], "下载中..."):
            # 创建一个临时字典和完成的字典
            temp_dict: dict = json_get["body"][ID]
            get_dict: dict = {"pid": int(ID), "p": temp_dict["pageCount"], "uid": temp_dict["userId"],
                              "title": temp_dict["title"], "author": temp_dict["userName"]}
            # r18主要是根据R-18标签进行判断，其他的这里不做考虑
            if "R-18" in temp_dict["tags"]:
                get_dict["r18"] = 1
            else:
                get_dict["r18"] = 0
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

    def getByTag(self, TAG: str, COOKIE, USER_AGENT, progress=gr.Progress()):
        keyword = quote(TAG)
        target = f"https://www.pixiv.net/ajax/search/artworks/{keyword}?word={keyword}&order=date_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": COOKIE,
            "user-agent": USER_AGENT,
            "referer": target,
        }
        session = requests.get(target, headers=headers, verify=False)
        session_json = session.json()

        permanent = session_json["body"]["popular"]["permanent"]

        # 创建一个空列表，用来储存json
        empty_arr = []

        for ITEM in progress.tqdm(permanent, "下载Popular中"):
            try:
                # 创建字典
                empty_dict: dict = {"pid": int(ITEM["id"]), "p": ITEM["pageCount"], "uid": ITEM["userId"],
                                    "title": ITEM["title"], "author": ITEM["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in ITEM["tags"]:
                    empty_dict["r18"] = 1
                else:
                    empty_dict["r18"] = 0
                empty_dict["width"] = ITEM["width"]
                empty_dict["height"] = ITEM["height"]
                empty_dict["tags"] = ITEM["tags"]
                # 通过ID转换为网址
                URL = f"https://www.pixiv.net/ajax/illust/{empty_dict['pid']}/pages?lang = zh"
                # 获取对应的图片链接
                session = requests.get(URL, headers=headers, verify=False)
                JSON1 = session.json()
                empty_dict["url"] = JSON1["body"][0]["urls"]["original"]
                empty_dict["urls"] = JSON1["body"][0]["urls"]
                empty_arr.append(empty_dict)
            except:
                continue
        with open(f"jsons/POPULAR_{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))

        # 另外一个
        recent = session_json["body"]["popular"]["recent"]
        for ITEM in progress.tqdm(recent, "下载Recent中"):
            try:
                empty_dict: dict = {"pid": int(ITEM["id"]), "p": ITEM["pageCount"], "uid": ITEM["userId"],
                                    "title": ITEM["title"], "author": ITEM["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in ITEM["tags"]:
                    empty_dict["r18"] = 1
                else:
                    empty_dict["r18"] = 0
                empty_dict["width"] = ITEM["width"]
                empty_dict["height"] = ITEM["height"]
                empty_dict["tags"] = ITEM["tags"]
                # 通过ID转换为网址
                URL = f"https://www.pixiv.net/ajax/illust/{empty_dict['pid']}/pages?lang = zh"
                # 获取对应的图片链接
                session = requests.get(URL, headers=headers, verify=False)
                JSON1 = session.json()
                empty_dict["url"] = JSON1["body"][0]["urls"]["original"]
                empty_arr.append(empty_dict)
            except:
                # 否则直接下一个就好
                continue
        with open(f"jsons/RECENT_{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return "下载完成！"

    def getByUser(self, TARGET: str,
                  COOKIE: str,
                  USER_AGENT: str,
                  progress=gr.Progress()):
        headers = {
            # 根据自己的浏览器情况填写，UA头也是
            "cookie": COOKIE,
            "user-agent": USER_AGENT,
            "referer": TARGET,
        }
        URL = TARGET
        session = requests.get(URL, headers=headers, verify=False)
        JSON = session.json()

        # 创建一个空列表，用来储存json
        empty_arr = []

        for ID in progress.tqdm(JSON["body"]["works"], "获取中"):
            # 因为随时会出现报错，所以加上一个判断，报错了直接跳过去就好~
            try:
                # 创建一个临时字典和空字典
                temp_dict: dict = JSON["body"]["works"][ID]
                empty_dict: dict = {"pid": int(ID), "p": temp_dict["pageCount"], "uid": temp_dict["userId"],
                                    "title": temp_dict["title"], "author": temp_dict["userName"]}
                # r18无法判断，这里先随便给一个把
                if "R-18" in temp_dict["tags"]:
                    empty_dict["r18"] = 1
                else:
                    empty_dict["r18"] = 0
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
            except:
                continue
        # 导出记录完毕的json数据
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return "下载完成！"
