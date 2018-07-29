# -*- coding: UTF-8 –*-
#coding:utf-8
'''
运行环境 anaconda3 python3
pip install googletrans
'''
import tkinter as tk
from googletrans import Translator
import sys

root = tk.Tk()
root.title("从福昕到谷歌翻译")
text_frame = tk.Frame(root)
text_frame.pack()
button_frame = tk.Frame(root)
button_frame.pack()


text1 = tk.Text(text_frame, height=30, width=40, font=("New Roman",18))

text1.pack(side=tk.LEFT)
text1.insert(tk.END, "1234")
text1.delete("0.0", tk.END)


text2 = tk.Text(text_frame, height=30, width=40, font=("New Roman",18))
scroll = tk.Scrollbar(root, command=text2.yview)
text2.configure(yscrollcommand=scroll.set)

text2.pack(side=tk.LEFT)
scroll.pack(side=tk.RIGHT, fill='y')

def drop_enter():
    global text1, text2
    text = text1.get("0.0", tk.END)
    text_out = []
    flag = 0
    for i, t in enumerate(text):
        if t != '\n':
            text_out.append(t)
        elif text[i-1] == '.':
            text_out.append(t)
        else:
            text_out.append(' ')

    text_out = ''.join(text_out)
    text1.delete("0.0", tk.END)
    text1.insert(tk.END, text_out)
	
def drop_space():
    global text1, text2
    text = text1.get("0.0", tk.END)
    text_out = []
    flag = 0
    for i, t in enumerate(text):
        if t != ' ':
            text_out.append(t)
        

    text_out = ''.join(text_out)
    text1.delete("0.0", tk.END)
    text1.insert(tk.END, text_out)
	
def translate():
    global text1, text2, translator
    text = text1.get("0.0", tk.END)
    res = translator.translate(text, dest='zh-CN').text
    text2.delete("0.0", tk.END)
    text2.insert(tk.END, res)
def clear1():
    global text1
    text1.delete("0.0", tk.END)
bt1 = tk.Button(button_frame, text="去回车", command=drop_enter)
bt1.grid(row=0, column=0)
bt2 = tk.Button(button_frame, text="翻译", command=translate)
bt2.grid(row=0, column=1)
bt2 = tk.Button(button_frame, text="清空1", command=clear1)
bt2.grid(row=0, column=2)
bt1 = tk.Button(button_frame, text="去空格", command=drop_space)
bt1.grid(row=0, column=4)

translator = Translator()
root.mainloop()