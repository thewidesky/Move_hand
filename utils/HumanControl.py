import keyboard
# import sys

# 这个py文件的目的是 实现通过电脑键盘等输入，输出想要的actions的命令
# actions的数据形式 是Franka机械臂的关节

class HumanController():
    actions = []
    keyboard_listening = False

    def __init__(self) -> None:
        self.actions = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] # 用于存放关节的指令,初始化
        
    # 开始监听键盘的输入
    def start_listen(self): # 获取从键盘输入的指令
        try:  
            if self.keyboard_listening == False: # 此时没有监听的话
                keyboard.hook(self.on_key_event)
                self.keyboard_listening = True
            else:
                pass
        except KeyboardInterrupt:
            print("程序被用户中断") 
    
    # 根据键盘的输入要处理的函数
    def on_key_event(self,event): 
        if event.name == 'esc' and event.event_type == 'down':
            # print("ESC被按下,键盘监听退出。")
            keyboard.unhook_all()
            # sys.exit() # 完成体记得删掉
        elif event.name == "a" and event.event_type == "down":
            # print("修改第一个命令数值。")
            self.change_first()
        elif event.name == "s" and event.event_type == "down":
            # print("修改第二个命令数值。")
            self.change_second()
        elif event.name == "d" and event.event_type == "down":
            # print("修改第三个命令数值。")
            self.change_third()
        elif event.name == "w" and event.event_type == "down":
            # print("修改第四个命令数值。")
            self.change_fourth()
        elif event.name == "j" and event.event_type == "down":
            # print("修改第五个命令数值。")
            self.change_fifth()
        elif event.name == "k" and event.event_type == "down":
            # print("修改第六个命令数值。")
            self.change_sixth()
        elif event.name == "l" and event.event_type == "down":
            # print("修改第七个命令数值。")
            self.change_seventh()
        elif event.name == "i" and event.event_type == "down":
            # print("修改第八个命令数值。")
            self.change_eigth()
        
    def change_first(self):
        # 没有设置panda_joint1,因为好像是基座，不需要设置
        # 修改第一个关节的指令，panda_joint2，default为-0.569,a
        # 往后面躺下，范围大概是-1--0
        if self.actions[1] > -1:
            self.actions[1] = self.actions[1] - 0.1
        else:
            pass
        # print(self.actions)

    def change_second(self):
        # 修改第二个关节的指令，panda_joint3，default为0.0，s
        # 腰部的旋转动作，范围大概是0--3
        if self.actions[2] < 3:
            self.actions[2] = self.actions[2] + 0.5
        else:
            pass
        # print(self.actions)
    
    def change_third(self):
        # 修改第三个关节的指令，panda_joint4，default为-2.810,d
        # 弯腰的动作，范围大概是-3--0
        if self.actions[3] > -3:
            self.actions[3] = self.actions[3] - 0.25
        else:
            pass
        # print(self.actions)
    
    def change_fourth(self):
        # 修改第四个关节的指令，panda_joint5，default为0.0，w
        # 整个上臂的旋转，取值范围是0--3
        if self.actions[4] < 3:
            self.actions[4] = self.actions[4] + 0.5
        else:
            pass
        # print(self.actions)
    
    def change_fifth(self):
        # 修改第五个关节的指令,pandan_joint6，default为3.037，j
        # 手臂的抬举动作，取值范围怀疑是0--5
        if self.actions[5] < 5:
            self.actions[5] = self.actions[5] + 0.5
        else:
            pass
        # print(self.actions)
    
    def change_sixth(self):
        # 修改第六个关节的指令,panda_joint7，default为0.741，k
        # 手臂的旋转关节，取值范围怀疑是0--1
        if self.actions[6] < 1:
            self.actions[6] = self.actions[6] + 0.1
        else:
            pass
        # print(self.actions)
    
    def change_seventh(self):
        # 修改第七和第八个关节的指令,panda_finger_joint1，default为0.04，l
        # 打开两个抓手，取值范围应该是0--0.05
        if self.actions[7] < 0.05 and self.actions[8] < 0.05:
            self.actions[7] = self.actions[7] + 0.01 # 增加了1/5的量
            self.actions[8] = self.actions[8] + 0.01
        else:
            pass
        # print(self.actions)
    
    def change_eigth(self):
        # 修改第七和第八个关节的指令,panda_finger_joint2，default为0.04，i
        # 握紧两个抓手，取值范围应该是0--0.05
        if self.actions[7] > 0 and self.actions[8] > 0:
            self.actions[7] = self.actions[7] - 0.01 # 增加了1/5的量
            self.actions[8] = self.actions[8] - 0.01 # 增加了1/5的量
        else:
            pass
        # print(self.actions)


# 机械手臂抓小球玩法解析：利用d来弯腰,j来抬起手臂，l来松开手臂，i来握紧手臂

# if __name__ == "__main__":
#     Control = HumanController() # 此处注意，一定要把实例建在外面
#     while(1): 
#         Control.start_listen()