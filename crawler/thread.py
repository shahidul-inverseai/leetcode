import threading


def func():
  pass 
  # print('called')

thread = threading.Timer(2, func)

thread.start()