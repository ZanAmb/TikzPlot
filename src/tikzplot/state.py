import __main__
import os.path

_export_counter = 0
_show_counter = 0
_imshow_counter = 0

def next_export_num():
    global _export_counter
    _export_counter += 1
    return _export_counter

def next_show_num():
    global _show_counter
    _show_counter += 1
    return _show_counter

def _next_imshow_num():
    global _imshow_counter
    _imshow_counter += 1
    return _imshow_counter

def main_name():
    return os.path.split(getattr(__main__, '__file__', None))