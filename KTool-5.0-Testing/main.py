import yaml
import gui as gui

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)

cookie = config['cookie']
user_agent = config['user_agent']
port = config['port']
db_name = config['db_name']

gui.get_gui(cookie, user_agent, db_name).launch(server_port=port)
