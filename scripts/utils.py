"""
工具类
实现一些基本的方法
"""
import os


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
