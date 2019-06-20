import threading


def run_in_background(func, *args):
    thread = threading.Thread(target=func, args=(*args,))
    thread.daemon = True
    thread.start()
