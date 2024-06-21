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
import wget
from urllib import parse

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
            print('jsons 文件夹不存在，已创建')
            os.mkdir('jsons')
        # 初始化data.json
        if not os.path.exists(f'jsons/{db_name}'):
            print(f'{db_name} 文件不存在，已创建')
            with open(f'jsons/{db_name}', 'w', encoding='utf-8') as f:
                f.write('[]')
        # 初始化pids文件-这个文件用于加快合并数据库的速度
        if not os.path.exists('pids.json'):
            print('pids.json 文件不存在，已创建')
            with open('pids.json', 'w', encoding='utf-8') as f:
                f.write('[]')
    except IOError:
        print('文件读写错误')
        return False
    finally:
        print('项目初始化完成！')
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
    print(f'追加完成！新增{files_counter}')
    return {'new': files_counter}


def stats_json(db_name: str) -> dict:
    print('处理中...不要着急')
    with open(f'jsons/{db_name}', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return {
        'length': len(data),
        'size': os.stat(f'jsons/{db_name}').st_size
    }