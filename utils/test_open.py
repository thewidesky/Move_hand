# 专门用于打开 模拟器 的py文件

from omni.isaac.lab.app import AppLauncher

# 运行环境
app_launcher = AppLauncher()
simulation_app = app_launcher.app

from omni.isaac.lab.utils import configclass
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg, ManagerBasedRLEnv

from source.standalone.move_hand_my.virtual_scene import SimpleSceneCfg
# from source.standalone.move_hand_my.utils.HumanControl import HumanController
from source.standalone.move_hand_my.actions import HumanControlJointActionsCfg
from source.standalone.move_hand_my.observations import ObservationCfg
from source.standalone.move_hand_my.utils.StoreDataToFile import create_HDF5_File, load_HDF5, Create_data_dict

import torch

@configclass
class VirtualEnvCfg(ManagerBasedRLEnvCfg):
    scene: SimpleSceneCfg = SimpleSceneCfg(num_envs=1, env_spacing=10.0) # 注意这里，也与scene有关
    actions: HumanControlJointActionsCfg = HumanControlJointActionsCfg()
    observations: ObservationCfg = ObservationCfg()

    def __post_init__(self):
        # 通常意味着原始信号的采样率被降低了4倍，以达到或接近50 Hz的控制或处理频率。
        # 在这个例子中，原始信号的采样率可能是200 Hz，然后通过4倍的降采样来达到50 Hz的控制或处理频率。
        self.decimation = 4  # env decimation -> 50 Hz control 设置环境降采样率，此处针对env
        # simulation settings 时间步长 dt 和频率 f 之间的关系为dt = 1 / f, 即0.005 = 1 /200
        self.sim.dt = 0.005  # simulation timestep -> 200 Hz physics  设置模拟时间步长，此处针对physics


def main():
    # 数据的文件存储的位置
    FileName = '/test1'
    FilePath = 'E:/Data/Move_hand_my/HDF5_data'
    data_dict = {
        '/observations/qpos': [],
        '/observations/images': [],
        }
    env = ManagerBasedRLEnv(cfg=VirtualEnvCfg())
    count = 0
    obs, _ = env.reset()
    while simulation_app.is_running():
        with torch.inference_mode():
            # reset
            if count % 300 == 0:
                # obs, _ = env.reset() # 暂时不重置
                print("-" * 80)
                print("[INFO]: 将要存储数据。。。")
                if count != 0:
                    # 将observation插入HDF5文件当中
                    create_HDF5_File(FileName,FilePath,data_dict)
            obs, rew, terminated, truncated, info = env.step(env.action_manager.action)
            # print("测试一下输出的观察：")
            # print(obs)
            count += 1
            Create_data_dict(data_dict, obs)
            # load_HDF5(FileName,FilePath) # 输出hdf5文件的数据，查看结果
            # break # 测试，只运行一次
    
    # close the environment
    env.close()

if __name__ == "__main__":
    main()
    simulation_app.close()