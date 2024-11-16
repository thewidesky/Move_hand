# Virtual_scene.py的主要目的就是构造出我们想要的  虚拟环境  的样子
# 主要的代码实在class SimpleSceneCfg当中
# 利用class VirtualEnvCfg与main()使得本py文件可以单独跑，从而查看我们所要构建的环境的真实样子

from __future__ import annotations

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.assets import AssetBaseCfg, RigidObjectCfg, ArticulationCfg
from omni.isaac.lab.assets import Articulation
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg, ManagerBasedRLEnv
from omni.isaac.lab.sensors import CameraCfg
from omni.isaac.lab.sim import PinholeCameraCfg
from omni.isaac.lab.utils import configclass

from source.standalone.move_hand_my.assets.all_assets import FRANKA_PANDA_CFG

import torch

# 构造我们想要的虚拟环境
# 记得要添加@configclass，否则会出现代码无法跑的情况
@configclass
class SimpleSceneCfg(InteractiveSceneCfg):

    # 地面
    ground = AssetBaseCfg(prim_path="/World/defaultGroundPlane", spawn=sim_utils.GroundPlaneCfg())

    # 光源
    dome_light = AssetBaseCfg(
        prim_path="/World/Light", spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
    )

    # 添加一个 桌面(立方体)，用于放置目标物体
    cube: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/cube",
        spawn=sim_utils.CuboidCfg(
            size=(1.0, 0.4, 0.3),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(max_depenetration_velocity=1.0, disable_gravity=False),
            collision_props= sim_utils.CollisionPropertiesCfg(collision_enabled=True),
            mass_props=sim_utils.MassPropertiesCfg(mass=10.0),
            physics_material=sim_utils.RigidBodyMaterialCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.5, 0.0, 0.0)),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.0, 0.75, 0.0)),
    )

    # 添加一个立方体，作为我们的抓取目标
    CubeTarget: RigidObjectCfg = RigidObjectCfg(
        prim_path="{ENV_REGEX_NS}/CubeTarget",
        spawn=sim_utils.CuboidCfg(
            size=(0.05, 0.05, 0.05),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(max_depenetration_velocity=1.0, disable_gravity=False),
            collision_props= sim_utils.CollisionPropertiesCfg(collision_enabled=True),
            mass_props=sim_utils.MassPropertiesCfg(mass=0.5),
            physics_material=sim_utils.RigidBodyMaterialCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 0.5)),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.0, 0.75, 0.4)),
    )

    # Franka机械臂
    franka: ArticulationCfg = FRANKA_PANDA_CFG.replace( # type: ignore
        prim_path="{ENV_REGEX_NS}/Franka",
        init_state = ArticulationCfg.InitialStateCfg(
            joint_pos={
                "panda_joint1": 0.0,
                "panda_joint2": -0.569,
                "panda_joint3": 0.0,
                "panda_joint4": -2.810,
                "panda_joint5": 0.0,
                "panda_joint6": 3.037,
                "panda_joint7": 0.741,
                "panda_finger_joint.*": 0.04,
        },
            pos=((0.0, 0.0, 0.0)),
            rot=((0.70711,0.0,0.0,0.70711)), # (w, x, y, z), Defaults to (1.0, 0.0, 0.0, 0.0) z轴旋转90度
        ),
    )


    # 添加一个摄像头，连接在Franka上，作为它的眼睛
    Camera: CameraCfg = CameraCfg(
        prim_path="{ENV_REGEX_NS}/Franka/Camera",
        spawn= PinholeCameraCfg(),
        # 设置Cmera的初始位置和角度，相对于父节点的偏移量
        offset= CameraCfg.OffsetCfg(
            pos=(0.4, 1.5, 0.5),
            rot= (-0.70711,0.0,0.0,0.70711),
            convention="world",
        ),
        width= 200, # Width of the image in pixels.
        height= 200,
    )