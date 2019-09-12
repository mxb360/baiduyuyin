#! python3

"""
文件 console.py
这个文件只适用于Python3.x
这个文件提供了python对Windows控制台的一些输入输出操作
它的功能类似于C语言中的 conio.h 头文件
通过这个文件可以：
	实现对控制台光标的移动
	实现输出有颜色的文字
	接收键盘的按键响应
	...

这些功能通过 Windows API 实现

作者：马小波
最近修改于：2017/12/09
版本：v2.1
"""

import ctypes as _ctypes

BLACK     = 0    # 黑色
BLUE      = 1    # 蓝色     
GREEN     = 2    # 绿色     
AQUA      = 3    # 浅绿色   
RED       = 4    # 红色     
PURPLE    = 5    # 紫色     
YELLOW    = 6    # 黄色     
WHITE     = 7    # 白色     
GRAY      = 8    # 灰色     
LBLUE     = 9    # 淡蓝色   
LGREEN    = 10   # 淡绿色   
LAQUA     = 11   # 淡浅绿色 
LRED      = 12   # 淡红色   
LPURPLE   = 13   # 淡紫色   
LYELLOW   = 14   # 淡黄色   
LWHITE    = 15   # 亮白色   

KEY_DOWN  = -1       # 方向键 上   
KEY_UP    = -2       # 方向键 下   
KEY_LEFT  = -3       # 方向键 左   
KEY_RIGHT = -4       # 方向键 右   
KEY_BACK  = 8        # 退格键 '\b' 
KEY_ENTER = 13       # 回车键 '\r' 
KEY_ESC   = 27       # Esc键       
KEY_TAB   = 9        # Tab键  '\t' 
KEY_SPACE = 32       # 空格键 ' '  

MATCH_CASE     = 0
NO_MATCH_CASE  = 1
ECHO_NOTHING   = 0
ECHO_STAR      = 1
ECHO_CHAR      = 2


class _COORD(_ctypes.Structure):
	_fields_ = [
		('Y', _ctypes.c_short),
		('X', _ctypes.c_short),
    ]


class _SMALL_RECT(_ctypes.Structure):
	_fields_ = [
		('Left', _ctypes.c_short), 
		('Top', _ctypes.c_short),
		('Right', _ctypes.c_short),
		('Bottom', _ctypes.c_short),
    ]


class _CONSOLE_SCREEN_BUFFER_INFO(_ctypes.Structure):
    _fields_ = [
        ('dwSize', _COORD),
        ('dwCursorPositions', _COORD),
        ('wAttributes', _ctypes.c_ushort),
        ('srWindow', _SMALL_RECT),
        ('dwMaximumWindowSize', _COORD),
    ]


class _Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

_STD_INPUT_HANDLE  = -10
_STD_OUTPUT_HANDLE = -11
_TRUE = 1
_FALSE = 0
_origin = _Coord(0, 0)
_axis = _Coord(1, 1)
_win_api = _ctypes.windll.kernel32
_hOut = _win_api.GetStdHandle(_STD_OUTPUT_HANDLE)
_use_color = True
_bInfo = _CONSOLE_SCREEN_BUFFER_INFO()
_win_api.GetConsoleScreenBufferInfo(_hOut, _ctypes.pointer(_bInfo))
_raw_bcolor = _bInfo.wAttributes >> 4
_raw_fcolor = _bInfo.wAttributes & 0x0f
_current_bcolor = _raw_bcolor
_current_fcolor = _raw_fcolor
_print = print

from sys import exit as _exit
from sys import stdout as _stdout
import os as _os
import msvcrt as _msvcrt


# # # # # # # # # # # # #
# Console API
# # # # # # # # # # # # #
def set_pos(x=0, y=0):
    coord = _COORD(_origin.x + _axis.x * x, _origin.y + _axis.x * y)
    _win_api.SetConsoleCursorPosition(_hOut, coord)

def get_pos():
    _win_api.GetConsoleScreenBufferInfo(_hOut, _ctypes.pointer(_bInfo))
    x = (_bInfo.dwCursorPositions.X - _origin.x) // _axis.x
    y = (_bInfo.dwCursorPositions.Y - _origin.y) // _axis.y
    return x, y

def set_fcolor(fcolor=_raw_fcolor):
    if _use_color:
        _win_api.GetConsoleScreenBufferInfo(_hOut, _ctypes.pointer(_bInfo))
        _win_api.SetConsoleTextAttribute(_hOut, (_bInfo.wAttributes & 0xf0) | (fcolor & 0x0f))
        _current_fcolor = fcolor

def set_bcolor(bcolor=_raw_bcolor):
    if _use_color:
        _win_api.GetConsoleScreenBufferInfo(_hOut, _ctypes.pointer(_bInfo))
        _win_api.SetConsoleTextAttribute(_hOut, (_bInfo.wAttributes & 0x0f) | (bcolor << 4))
        _current_bcolor = bcolor

def set_origin(x=0, y=0):
    _origin = x, y

def get_origin():
    return _origin.x, _origin.y

def set_axis(dx=1, dy=1):
    _axis = dx, dy

def get_axis():
    return _axis.x, _axis.y

def reset():
    _win_api = _ctypes.windll.kernel32
    _hOut = _win_api.GetStdHandle(_STD_OUTPUT_HANDLE)
    set_axis()
    set_origin()
    set_bcolor()
    set_fcolor()
    _use_color = True

def print(value, fcolor=None, sep=''):
    if fcolor is not None:
        global _current_fcolor
        current_fcolor = _current_fcolor
        set_fcolor(fcolor)
    _print(value, sep=sep, end='', flush=True)
    if fcolor is not None:
        set_fcolor(current_fcolor)

def use_color(use_color=True):
    _use_color = use_color

def have_key():
    return _msvcrt.kbhit()

def sleep(ms):
    return _win_api.Sleep()

def clear():
    return _os.system('cls')

def pause(str=''):
    if str is None:
        return _os.system('pause')
    print(str)
    return _os.system('pause>nul')

def get_key(case):
    key = _msvcrt.getch()
    if key == b'\0xe0':
        key = _msvcrt.getch()
        if key == b'H':
            return KEY_UP
        if key == b'P':
            return KEY_DOWN
        if key == b'K':
            return KEY_LEFT
        if key == b'M':
            return KEY_RIGHT
    elif case:
        key = key.decode('gbk')
    else:
        key = key.decode('gbk').upper()
    return key

# # # # # # # # # # # # #
# Console Init
# # # # # # # # # # # # #
reset()

# # # # # # # # # # # # #
# Console API Test
# # # # # # # # # # # # #
if __name__ == '__main__':
    set_pos(3, 3)
    set_fcolor(LRED)
    print('hello', '2')
    set_fcolor()
    print('hello', get_pos())

    while True:
        get_key(True)
