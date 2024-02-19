import tkinter as tk
import _thread
from utils.kaede import mergeJsonFiles, Init


# 创建一个选择器，根据模式选择需要的函数
def modeGate(_mode, _url) -> None:
    match _mode.get():
        case 'ILL':
            _thread.start_new_thread(pixiv.getByIllusts, (_url.get(),))
        case 'USR':
            _thread.start_new_thread(pixiv.getByUser, (_url.get(),))
        case 'TAG':
            _thread.start_new_thread(pixiv.getByTag, (_url.get(),))
        case _:
            print('参数错误')


# 初始化，判断是否存在
pixiv = Init()

# 创建界面
root = tk.Tk()

# 窗口相关
root.title('KTool-Pixiv TK!')
root.geometry('458x213')

# 创建几个变量
mode = tk.StringVar(value='USR')
url = tk.StringVar()
# 提示框
tk.Label(root, text='Choose the mode you want').pack()

# 选择
tk.Radiobutton(root, text='Via Illust', variable=mode, value='ILL').pack()
tk.Radiobutton(root, text='Via User', variable=mode, value='USR').pack()
tk.Radiobutton(root, text='Via Tag', variable=mode, value='TAG').pack()

tk.Label(root, text='Input url you need').pack()
tk.Entry(root, textvariable=url).pack()

# 开始按钮
tk.Button(root, text='=GET=', command=lambda: modeGate(mode, url)).pack()
tk.Button(root, text='=Merge Files=', command=lambda: mergeJsonFiles()).pack()

root.mainloop()
