# 实现了对于 键盘输入的简单使用
import keyboard
import time
import sys

def on_key_event(event):
    if event.event_type == 'up': # 弹起来的时候
        print(f'用户不再一直按着{event.name}键，{event.event_type}')
        keyboard.unhook_all() # 不再监听

    elif event.name == 'esc' and event.event_type == 'down':
        print("监听即将停止,因为按下了ESC键。")
        keyboard.unhook_all()
        sys.exit() # 直接结束整个main程序

    else: # 按下的时候
        print(f"用户一直按着{event.name} {event.event_type}")

if __name__ == "__main__":
    while(1): # 此处需要不断的循环才能不断的hook，需要慎重思考结束方法
        keyboard.hook(on_key_event)
        time.sleep(1)