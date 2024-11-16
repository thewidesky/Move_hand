import h5py
import numpy as np
import os

# 查看了一下，别人的h5py文件是一个怎么样的结构
# f = h5py.File('E:/Data/Aloha-act/sim_transfer_cube_scripted/episode_0.hdf5', mode='r') 
# list = list(f.keys()) #查看键值
# print(list)

# 打开HDF5文件
with h5py.File('E:/Data/Aloha-act/sim_transfer_cube_scripted/episode_0.hdf5', 'r') as f:
    # 查看文件中的数据集
    for name in f:
        print("name",name)

    # 读取数据集
    dataset = f['action']

    # 查看数据集的属性
    for key in dataset.attrs:
            print("dataset.attrs:/n",key, dataset.attrs[key])

    data = dataset[:]
    print("data",data)
