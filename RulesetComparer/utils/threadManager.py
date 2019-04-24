import threading


def run_in_background(func, parameter):
    thread = threading.Thread(target=func, args=(parameter,))
    thread.daemon = True
    thread.start()
