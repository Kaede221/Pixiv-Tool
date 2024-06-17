import yaml
import utils as utils

# 读取配置文件
with open('config.yaml', 'r', encoding='UTF-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# 初始化项目
utils.init_project(config['db_name'])
# 实例化Pixiv
pixiv = utils.Pixiv(config['cookie'], config['user_agent'])


# 函数，用于区分
def mode_gate(mode: str, _target: str):
    match mode:
        case "Ill":
            pixiv.get_by_illusion(_target)
        case "User":
            pixiv.get_by_user(_target)
        case "Tag":
            pixiv.get_by_tag(_target)


def main_getter(mode:str):
    while True:
        _url = input('url > ')
        if _url == 'exit':
            break
        elif _url == '':
            continue
        mode_gate(mode, _url)
        print("== Done ==")

while True:
    print("======操作======")
    print("1. Ill")
    print("2. User")
    print("3. Tag")
    print("======工具======")
    print("4. Merge Files")
    print("5. Stats data.json")
    print("================")
    print("6. exit")
    print("================")
    choose: int = int(input("选择 > "))
    match choose:
        case 1:
            main_getter('Ill')
        case 2:
            main_getter('User')
        case 3:
            main_getter('Tag')
        case 4:
            utils.merge_json_files(config['db_name'])
        case 5:
            _stats = utils.stats_json(config['db_name'])
            print(f"数据量：{_stats['length']}，文件大小：{_stats['size']}")
        case 6:
            break
