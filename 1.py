
# добавить при работе с джойстиком 
from sys import platform
if platform == "linux" or platform == "linux2":
    print("linux")
elif platform == "darwin":
    print('mac')
elif platform == "win32":
    print('windows')