# 用于观测数据的输出,即observations

from omni.isaac.lab.managers import ObservationGroupCfg as ObsGroup
from omni.isaac.lab.managers import ObservationTermCfg as ObsTerm
# import omni.isaac.lab.envs.mdp.observations as mdpobs 

from omni.isaac.lab.assets import Articulation, RigidObject
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.envs import ManagerBasedEnv, ManagerBasedRLEnv
from omni.isaac.lab.sensors import Camera

from omni.isaac.lab.utils.noise import AdditiveUniformNoiseCfg as Unoise
from omni.isaac.lab.utils import configclass

import torch


# 注意修改"franka"，不然可能会报错
def joint_pos(env: ManagerBasedEnv, asset_cfg: SceneEntityCfg = SceneEntityCfg("franka")) -> torch.Tensor:
    """The joint positions of the asset.

    Note: Only the joints configured in :attr:`asset_cfg.joint_ids` will have their positions returned.
    """
    # extract the used quantities (to enable type-hinting)
    asset: Articulation = env.scene[asset_cfg.name]
    return asset.data.joint_pos[:, asset_cfg.joint_ids]


# 获取Camera
def get_image(env: ManagerBasedEnv, sensors_cfg: SceneEntityCfg = SceneEntityCfg("Camera")) -> torch.Tensor:
    sensor: Camera = env.scene[sensors_cfg.name]
    # 先输出图片的shape进行简单的测试
    # camera_shape = torch.tensor(sensor.camera_shape)

    # RGB三个颜色通道外，还有一个通常是Alpha通道（也称透明度通道）
    image = sensor.data.output["rgb"]
    return image



@configclass
class ObservationCfg:

    @configclass
    class SimpleCfg(ObsGroup): # 可以建立多个观察组，即ObsGroup

        base_pos_z = ObsTerm(
            # The joint positions of the asset
            func = joint_pos,
            # 通过模拟真实世界中的传感器噪声，系统可以在训练时学习到如何处理这些不确定性，从而提高在实际应用中的鲁棒性。
            # noise = Unoise(n_min=-0.1, n_max=0.1),
            # 剪切操作可以限制观测值的范围，防止极端值对模型训练造成不利影响。过滤异常数值
            # clip = (-100.0, 100.0),
            # 缩放观测数据可以使不同特征的尺度一致，这有助于模型更快地学习和收敛。？？？
            # scale = 1.0,
        )

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True
    
    @configclass
    class ImageObsCfg(ObsGroup):

        Image = ObsTerm(
            func = get_image,
        )

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True
    
    # observation groups
    Simple: SimpleCfg = SimpleCfg() # 机械臂关机的动作
    Image: ImageObsCfg = ImageObsCfg() # camera的RGB加透明度矩阵