import streamlit as st

from scripts.pixiv import Pixiv
from scripts.utils import *

# 读取配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

# 初始化项目
init_project('data.json')

# 实例化
pixiv = Pixiv(config['user']['cookie'], config['user']['userAgent'])

# 主页UI
st.markdown('# Pixiv Tool')

# Tabs
tab1, tab2 = st.tabs(['获取', '处理'])

# 获取数据相关
with tab1:
    mode = st.radio('获取方式', ['Ill', 'User'])
    target_url = st.text_input('目标链接')
    if st.button('开始获取', use_container_width=True):
        pixiv.mode_gate(mode, target_url)

with tab2:
    st.markdown('### 合并文件')
    st.text_input('输出文件名', 'data.json', disabled=True)
    if st.button('开始合并文件'):
        st.write(merge_json_files('data.json'))
    if st.button('查看数据库相关数据'):
        st.write(stats_json('data.json'))
