import threading
import itertools
import time
import sys


class Signal:
    """通过类属性控制循环"""
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    """1. itertools.cycle循环迭代|/-\\"""
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        """
        2. sys.stdout.flush刷新输出
        不等待字符送到缓冲区一起打印
        """
        flush()
        """3. 通过\x08退格来删除过期字符"""
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break


def slow_function():
    # 假装等待I/O一段时间
    time.sleep(3)
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin,
                               args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
