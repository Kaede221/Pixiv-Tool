import json
import time

import requests
import gradio as gr


def get_image_url(url: str, headers: dict):
    new_json = requests.get(url, headers=headers, verify=False).json()
    return new_json["body"][0]["urls"]["original"]


def get_operated_data(json_data: dict, pid: str, headers: dict) -> dict:
    temp_dict: dict = json_data["body"]['works'][pid]
    url = f"https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh"
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
    def __init__(self, cookie, user_agent):
        self.cookie = cookie
        self.userAgent = user_agent

    def get_header(self, target_url: str) -> dict:
        return {
            "cookie": self.cookie,
            "user-agent": self.userAgent,
            "referer": target_url,
        }

    def get_by_illusion(self, target_url: str, progress=gr.Progress()):
        headers = self.get_header(target_url)
        json_get = requests.get(target_url, headers=headers, verify=False).json()
        empty_arr = []
        err_count = 0
        try:
            # 获取数据
            for ID in progress.tqdm(json_get["body"], "下载中..."):
                empty_arr.append(get_operated_data(json_get, ID, headers))
        except:
            err_count += 1
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return f'下载完成, 失败数量: {err_count}'

    def get_by_user(self, target_url: str, progress=gr.Progress()):
        headers = self.get_header(target_url)
        empty_arr = []
        err_count = 0
        try:
            json_data = requests.get(target_url, headers=headers, verify=False).json()
            for ID in progress.tqdm(json_data["body"]["works"], "获取中"):
                empty_arr.append(get_operated_data(json_data, ID, headers))
        except:
            err_count += 1
        with open(f"jsons/{time.time()}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(empty_arr))
        return f"下载完成, 失败数量: {err_count}"

    def mode_gate(self, mode: str, target_url: str):
        match mode:
            case 'User':
                return self.get_by_user(target_url)
            case 'Ill':
                return self.get_by_illusion(target_url)
