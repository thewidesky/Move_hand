# 参考网址
# https://www.cnblogs.com/-wenli/p/14020264.html

import h5py
import numpy as np
import os

def main():
     # 获取当前工作目录  
    current_directory = os.getcwd()  
    print("当前工作目录是:", current_directory)

    #===========================================================================
    # Create a HDF5 file.
    path = current_directory + '/source/standalone/move_hand_my/utils/test/'
    path_last = path + 'h5py_example.hdf5'
    # f = h5py.File("h5py_example.hdf5", "w")    # mode = {'w', 'r', 'a'}
    f = h5py.File(path_last, "w")

    # Create two groups under root '/'.
    g1 = f.create_group("bar1")
    g2 = f.create_group("bar2")

    # Create a dataset under root '/'.
    d = f.create_dataset("dset", data=np.arange(16).reshape([4, 4]))

    # Add two attributes to dataset 'dset'
    # Attributes 为该 dataset 的其他自定义属性
    d.attrs["myAttr1"] = [100, 200]
    d.attrs["myAttr2"] = "Hello, world!"

    # Create a group and a dataset under group "bar1".
    c1 = g1.create_group("car1")
    d1 = g1.create_dataset("dset1", data=np.arange(10))

    # Create a group and a dataset under group "bar2".
    c2 = g2.create_group("car2")
    d2 = g2.create_dataset("dset2", data=np.arange(10))

    # Save and exit the file.
    f.close()

    ''' h5py_example.hdf5 file structure
    +-- '/'
    |   +-- group "bar1"
    |   |   +-- group "car1"
    |   |   |   +-- None
    |   |   |   
    |   |   +-- dataset "dset1"
    |   |
    |   +-- group "bar2"
    |   |   +-- group "car2"
    |   |   |   +-- None
    |   |   |
    |   |   +-- dataset "dset2"
    |   |   
    |   +-- dataset "dset"
    |   |   +-- attribute "myAttr1"
    |   |   +-- attribute "myAttr2"
    |   |   
    |   
    '''

    #===========================================================================
    # Read HDF5 file.
    # f = h5py.File("h5py_example.hdf5", "r")    # mode = {'w', 'r', 'a'}
    f = h5py.File(path_last, "r")

    # Print the keys of groups and datasets under '/'.
    print("文件的名字是：")
    print(f.filename)
    print("文件内部的一级目录为：")
    print([key for key in f.keys()], "\n")  

    #===================================================
    # Read dataset 'dset' under '/'.
    d = f["dset"]

    # Print the data of 'dset'.
    print(d.name, ":")
    print(d[:])

    # Print the attributes of dataset 'dset'.
    for key in d.attrs.keys():
        print(key, ":", d.attrs[key])

    print()

    #===================================================
    # Read group 'bar1'.
    g = f["bar1"]

    # Print the keys of groups and datasets under group 'bar1'.
    print([key for key in g.keys()])

    # Three methods to print the data of 'dset1'.
    print("三种访问文件Path的示例:")
    print(f["/bar1/dset1"][:])        # 1. absolute path

    print(f["bar1"]["dset1"][:])    # 2. relative path: file[][]

    print(g['dset1'][:])        # 3. relative path: group[]



    # Delete a database.
    # Notice: the mode should be 'a' when you read a file.
    '''
    del g["dset1"]
    '''

    # Save and exit the file
    f.close()

    print("finished all")

if __name__ == "__main__":
    main()
