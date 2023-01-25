import threading

class ThreadController:
    def __init__(self, thread_max):
        self.thread_max = thread_max
        self.loaded_threads = []

    def start_load_wait(self, method):
        self.load_threads(method)
        self.start_all_threads()
        self.wait_for_all_threads()

    def load_threads(self, method):
        for index in range(0, self.thread_max, 1):
            self.loaded_threads.append(threading.Thread(target=method, args=(index,)))

    def start_all_threads(self):
        for thread in self.loaded_threads:
            thread.start()

    def wait_for_all_threads(self):
        for thread in self.loaded_threads:
            thread.join()