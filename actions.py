# 用于建造actions的函数，测试是否能够给 机器人动作
# 这里使用的是 由force进行控制

from __future__ import annotations

from collections.abc import Sequence

from omni.isaac.lab.assets import Articulation
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg, ManagerBasedRLEnv
from omni.isaac.lab.managers.action_manager import ActionTerm, ActionTermCfg
from omni.isaac.lab.utils import configclass

from source.standalone.move_hand_my.utils.HumanControl import HumanController

import torch
import carb

class HumanControlJointActionTerm(ActionTerm):
    cfg: HumanControlJointEffortActionCfg
    _asset: Articulation
    controller = HumanController()

    def __init__(self, cfg: HumanControlJointEffortActionCfg, env: ManagerBasedRLEnv) -> None:
        # initialize the action term
        super().__init__(cfg, env)

        # resolve the joints over which the action term is applied
        self._joint_ids, self._joint_names = self._asset.find_joints(self.cfg.joint_names)
        self._num_joints = len(self._joint_ids)
        # log the resolved joint names for debugging
        carb.log_info(
            f"Resolved joint names for the action term {self.__class__.__name__}:"
            f" {self._joint_names} [{self._joint_ids}]"
        )

        # Avoid indexing across all joints for efficiency
        if self._num_joints == self._asset.num_joints:
            self._joint_ids = slice(None)

        # create tensors for raw and processed actions
        self._raw_actions = torch.zeros(self.num_envs, self.action_dim, device=self.device)
        self._processed_actions = torch.zeros_like(self.raw_actions)

    """
    Properties.
    """

    @property
    def action_dim(self) -> int:
        return self._num_joints

    @property
    def raw_actions(self) -> torch.Tensor:
        return self._raw_actions

    @property
    def processed_actions(self) -> torch.Tensor:
        return self._processed_actions

    """
    Operations.
    """

    def process_actions(self, actions: torch.Tensor):
        # store the raw actions
        self._raw_actions[:] = actions
        # apply the affine transformations
        self.controller.start_listen()
        self._processed_actions = torch.tensor(self.controller.actions)

    def reset(self, env_ids: Sequence[int] | None = None) -> None:
        self._raw_actions[env_ids] = 0.0 # reset是否要全部重置为0，有待争议


    def apply_actions(self):
        # set joint effort targets
        # print("将要给的actions是:")
        # print(self.processed_actions)
        self._asset.set_joint_position_target(self.processed_actions, joint_ids=self._joint_ids)


@configclass
class HumanControlJointEffortActionCfg(ActionTermCfg):
    class_type: type[ActionTerm] = HumanControlJointActionTerm
    asset_name = "franka"
    joint_names = ["panda_joint1","panda_joint2","panda_joint3",
                   "panda_joint4","panda_joint5","panda_joint6","panda_joint7",
                   "panda_finger_joint1","panda_finger_joint2"]


# 最后在环境中应用的action的class
@configclass
class HumanControlJointActionsCfg:
    joint_Effort = HumanControlJointEffortActionCfg()