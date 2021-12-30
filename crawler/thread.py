import threading


def func():
  print('called')

thread = threading.Timer(2, func)

thread.start()