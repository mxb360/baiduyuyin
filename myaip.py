import argparse
import console as con
import sys

def print_error(err_str):
    con.print('%s: 错误: %s' % ('myaip', err_str), con.LRED)

try:
    from aip import AipSpeech
except ImportError:
    print_error("没有找到百度语音PythonSDK，请考虑：\n   pip install baidu-aip\n")
    sys.exit(-1)

def cammandline():
    parser = argparse.ArgumentParser(description="语音合成")    
    parser.add_argument('-v', action='store_true', dest='is_verbose',
                    help='produce verbose output')
    parser.add_argument('-o', action='store', dest='output',
                    metavar='FILE',
                    help='direct output to FILE instead of stdout')
    parser.add_argument('-C', action='store', type=int, dest='context',
                    metavar='NUM', default=0,
                    help='display NUM lines of added context')
    args = parser.parse_args() 

    print(args.__dict__)

cammandline()