"""
使用Streamlit进行重构
进度条在控制台显示
"""
import streamlit as st
import utils as utils
import yaml

"""
# KTool 5.0
Powered by Streamlit
"""

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)

cookie = config['cookie']
user_agent = config['user_agent']
db_name = config['db_name']

# 初始化项目
utils.init_project(db_name)

# 实例化pixiv对象
pixiv = utils.Pixiv(cookie, user_agent)

# 用户界面
tab_get, tab_deal = st.tabs(['获取', '处理'])

with tab_get:
    choose_mode = st.selectbox('获取方式', ['Ill', 'User', 'Tag'],
                               help='获取数据的方式，允许通过Ill，User或者Tag进行获取')
    target_url_or_tag = st.text_input("目标链接或Tag",
                                      help="可以输入目标链接，链接形如https://www.pixiv.net/ajax/user/11261350/profile/illusts?ids")
    get_button = st.button('开始获取', key='get_button', type='primary', use_container_width=True)

    if get_button:
        pixiv.mode_gate(choose_mode, target_url_or_tag)

with tab_deal:
    target_database_name = st.text_input('数据库文件名', db_name, help='目标数据库的文件名称，请在config.yaml进行修改',
                                         disabled=True)
    merge_button = st.button('合并文件', key='merge_button', type='primary', use_container_width=True)
    states_button = st.button('查看数据库相关数据', use_container_width=True)
    if merge_button:
        ret = utils.merge_json_files(target_database_name)
        st.write(ret)
    if states_button:
        ret = utils.stats_json(target_database_name)
        st.write(ret)
