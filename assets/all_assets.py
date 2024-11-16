import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.actuators import ActuatorNetMLPCfg, DCMotorCfg, ImplicitActuatorCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg


# ISAACLAB_NUCLEUS_DIR是本地地址
from omni.isaac.lab.utils.assets import ISAACLAB_NUCLEUS_DIR,ISAAC_NUCLEUS_DIR,NVIDIA_NUCLEUS_DIR

# Franka机械臂的样子
FRANKA_PANDA_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/FrankaEmika/panda_instanceable.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False, 
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        ),
        # collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        # 一共是7=?个关节
        # 以我现有知识，暂时无法看出 各个关节的界限值 是多少。
        # 若全是旋转关节，则取值应该为(0,2*pi),对应为(0,360度)
        joint_pos={
            "panda_joint1": 0.0, # 0.0,
            "panda_joint2": 0.0, # -0.569,
            "panda_joint3": 0.0, # 0.0,
            "panda_joint4": 0.0, # -2.810,

            "panda_joint5": 0.0, # 0.0,
            "panda_joint6": 0.0, # 3.037,
            "panda_joint7": 0.0, # 0.741,

            "panda_finger_joint.*": 0.1, # 0.04,
        },
    ),
    actuators={
        # shoulder 肩膀
        "panda_shoulder": ImplicitActuatorCfg(
            joint_names_expr=["panda_joint[1-4]"],
            effort_limit=87.0, # 驱动器可以施加的最大力或力矩限制
            velocity_limit=2.175, # 关节的最大速度限制
            stiffness=80.0, # 驱动器的刚度，即驱动器抵抗外部扰动的能力。
            damping=4.0, # 驱动器的阻尼，即驱动器在运动时消耗能量的能力
        ),
        # forearm 前臂
        "panda_forearm": ImplicitActuatorCfg(
            joint_names_expr=["panda_joint[5-7]"],
            effort_limit=12.0,
            velocity_limit=2.61,
            stiffness=80.0,
            damping=4.0,
        ),
        # 手部
        "panda_hand": ImplicitActuatorCfg(
            joint_names_expr=["panda_finger_joint.*"],
            effort_limit=200.0,
            velocity_limit=0.2,
            stiffness=2e3,
            damping=1e2,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of Franka Emika Panda robot."""


FRANKA_PANDA_HIGH_PD_CFG = FRANKA_PANDA_CFG.copy() # type: ignore
FRANKA_PANDA_HIGH_PD_CFG.spawn.rigid_props.disable_gravity = True
FRANKA_PANDA_HIGH_PD_CFG.actuators["panda_shoulder"].stiffness = 400.0
FRANKA_PANDA_HIGH_PD_CFG.actuators["panda_shoulder"].damping = 80.0
FRANKA_PANDA_HIGH_PD_CFG.actuators["panda_forearm"].stiffness = 400.0
FRANKA_PANDA_HIGH_PD_CFG.actuators["panda_forearm"].damping = 80.0
"""Configuration of Franka Emika Panda robot with stiffer PD control.

This configuration is useful for task-space control using differential IK.
"""