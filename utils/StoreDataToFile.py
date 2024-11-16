# 此py文件的目的是为了测试实现，将从 observation观测到的数据存储至一个File文件当中，从未实现更加方便地复用。

import h5py

# 我现在想要的HDF5文件的结构：
'''
/observations/qpos
/observations/images
'''

# 与HDF5文件的结构保持一致
# data_dict = {
#             '/observations/qpos': [],
#             '/observations/images': [],
# }

def Create_data_dict(data_dict, obs):
    # 根据字典结构插入数据,obs要是外部传来的observation
    data_dict['/observations/qpos'].append(obs['Simple']) # "Simple"与observation的命令有关
    data_dict['/observations/images'].append(obs['Image']) # "Image"与observation的命令有关
    return data_dict
    

# 主要是要构造出想要的HDF5文件的结构
def create_HDF5_File(FileName, FilePath, data_dict_obs):
    # 获取一共有多少个时间次数，即/observations/qpos一共有多少个
    time_number = len(data_dict_obs['/observations/qpos'])
    # print(time_number)

    # 创建HDF5文件
    Total_Path = FilePath + FileName
    with h5py.File(Total_Path + '.hdf5', 'w', rdcc_nbytes=1024 ** 2 * 2) as root: # rdcc_nbytes 缓存大小
        # 创造数据文件结构
        observations = root.create_group('observations')
        qpos = observations.create_dataset('qpos', (time_number,1, 9)) # qpos的shape：(1,9) 1这里是1个环境
        images = observations.create_dataset('images', (time_number,1, 200,200,4)) # image的shape：(1,200,200,4)
        # 正式插入数据
        for name, array in data_dict_obs.items():
            # print("The array is:",array)
            root[name][...] = array[0].cpu().numpy() # 因为hdf5不能存储cuda0的数据
    # print("创建完毕")


def load_HDF5(FileName, FilePath):
    Total_Path = FilePath + FileName
    with h5py.File(Total_Path + '.hdf5', 'r') as root:
        qpos = root['observations/qpos']
        images = root['observations/images']
        print("qpos is:",qpos[:])
        print("images is:",images[:])
    print("数据输出完毕")