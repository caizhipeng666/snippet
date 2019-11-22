import threading
import contextlib
from queue import Queue


class ThreadPool(object):
    def __init__(self, maxsize=10):
        self.queue = Queue()
        self.maxsize = maxsize
        self.stop_flag = False
        self.quit_flag = False
        self.daemon = False

        self.__thread_list = []
        self.__free_list = []
        self.result_list = []

    def __iter__(self):
        return iter(self.result_list)

    def submit(self, func, args=None, callback=None):
        self.__create_thread()
        task = (func, args, callback)
        self.queue.put(task)

    def close(self):
        full_size = len(self.__thread_list)
        while full_size:
            self.queue.put(self.stop_flag)
            full_size -= 1

    def quit(self):
        self.quit_flag = True
        while self.__thread_list:
            self.queue.put(self.stop_flag)
        self.queue.queue.clear()

    def join(self):
        for t in self.__thread_list:
            t.join()

    def __create_thread(self):
        if len(self.__free_list) == 0 and len(self.__thread_list) < self.maxsize:
            t = threading.Thread(target=self.__call, daemon=self.daemon)
            t.start()
            self.__thread_list.append(t)

    def __call(self):
        current_thread = threading.current_thread()
        event = self.queue.get()
        while event != self.stop_flag:
            func, args, callback = event
            try:
                result = func(*args)
                func_execute_status = True
                self.result_list.append(result)
            except Exception as e:
                result = None
                func_execute_status = False
                print('函数执行产生错误', e)

            if func_execute_status:
                if callback:
                    try:
                        callback(result)
                    except Exception as e:
                        print('回调函数执行产生错误', e)

            with self.__free_state(self.__free_list, current_thread):
                # 执行完一次任务后，将线程加入空闲列表。然后继续去取任务，如果取到任务就将线程从空闲列表移除
                if self.quit_flag:
                    event = self.stop_flag
                else:
                    event = self.queue.get()

        else:
            self.__thread_list.remove(current_thread)

    @contextlib.contextmanager
    def __free_state(self, state_list, worker_thread):
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)


if __name__ == '__main__':
    def Foo(arg):
        return arg

    def Bar(res):
        print(res)


    pool = ThreadPool(5)
    for i in range(10):
        pool.submit(func=Foo, args=(i,), callback=Bar)
    pool.close()
    pool.join()
    pool.quit()

    print("任务队列里任务数%s" % pool.queue.qsize())
    print("当前存活子线程数量:%d" % threading.activeCount())
    for r in pool:
        print(r)
