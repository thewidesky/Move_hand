# 文心一言给的几乎完美的例子

import keyboard  
import threading  
import time  
  
# 布尔变量，用于跟踪键盘监听状态  
keyboard_listening = False  
  
# 定义一个函数来处理按键事件  
def on_key_event(event):  
    print(f"Key {event.name} pressed.")  
  
# 设置一个线程锁，以确保线程安全地修改keyboard_listening变量  
lock = threading.Lock()  
  
# 定义一个函数来启动键盘监听  
def start_keyboard_listening():  
    with lock:  
        global keyboard_listening  
        if not keyboard_listening:  
            # 设置键盘监听器  
            keyboard.on_press(on_key_event)  
            # 注意：keyboard.on_press()是持续监听的，不需要显式地启动一个循环  
            # 如果你需要停止监听，应该调用keyboard.unhook_all()  
            keyboard_listening = True  
            print("Keyboard listening started.")  
        else:  
            print("Keyboard is already listening.")  
  
# 定义一个函数来停止键盘监听  
def stop_keyboard_listening():  
    with lock:  
        global keyboard_listening  
        if keyboard_listening:  
            # 停止所有键盘监听器  
            keyboard.unhook_all()  
            keyboard_listening = False  
            print("Keyboard listening stopped.")  
        else:  
            print("Keyboard is not listening.")  
  
# 示例：启动键盘监听  
start_keyboard_listening()  
# 让程序运行一段时间，以便你可以测试键盘监听  
time.sleep(20)  
  
# 停止键盘监听  
stop_keyboard_listening()