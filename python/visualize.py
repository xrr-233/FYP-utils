"""
用来做文件的可视化专用
"""

import pickle
import open3d as o3d
import numpy as np
from utils import CameraPoseVisualizer, load_K_Rt_from_P

def render_point_cloud(path):
    """
    渲染点云
    :param path: 输入文件路径（.ply） # e.g. path = 'outputs/mvsnet001_l3.ply'
    :return:
    """
    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud(path)
    print(dir(pcd))
    points = np.asarray(pcd.points)
    print(points)
    print(np.max(points, axis=0))
    print(np.min(points, axis=0))
    o3d.visualization.draw_geometries([pcd])

def render_mesh(path):
    """
    渲染网格
    :param path: 输入文件路径（.ply/.off） # e.g. ply_path = 'data/demo/Matterport3D_processed/17DRP5sb8fy/pointcloud.ply'
    :return:
    """
    print("Testing mesh in Open3D...")
    mesh = o3d.io.read_triangle_mesh(path)
    print(mesh)
    print("Computing normal and rendering it.")
    mesh.compute_vertex_normals()
    print(np.asarray(mesh.triangle_normals))
    o3d.visualization.draw_geometries([mesh])

def load_npz(path):
    """
    打印在npz格式的数据中存在的所有类dict属性
    :param path: # e.g. npz_path = 'data/demo/Matterport3D_processed/17DRP5sb8fy/pointcloud.npz'
    :return:
    """
    print("Load an npz file and print it")
    npz_point_cloud = np.load(path)
    for key in npz_point_cloud:
        print(key)
        print(npz_point_cloud[key].shape)

def render_camera_extrinsic_params(path):
    """
    如题，渲染相机外参（位姿）
    :param path:
    :return:
    """
    npz = np.load(path)
    n_images = int(len(npz) / 6)

    # world_mat is a projection matrix from world to image
    world_mats_np = [npz[f'world_mat_{idx}'].astype(np.float32) for idx in range(n_images)]

    # scale_mat: used for coordinate normalization, we assume the scene to render is inside a unit sphere at origin.
    scale_mats_np = [npz[f'scale_mat_{idx}'].astype(np.float32) for idx in range(n_images)]

    intrinsics_all = []
    pose_all = []

    for scale_mat, world_mat in zip(scale_mats_np, world_mats_np):
        P = world_mat @ scale_mat
        P = P[:3, :4]
        intrinsics, pose = load_K_Rt_from_P(None, P)
        intrinsics_all.append(intrinsics)
        pose_all.append(pose)

    print(pose_all[0])
    min_x = max_x = pose_all[0][0, 3]
    min_y = max_y = pose_all[0][1, 3]
    min_z = max_z = pose_all[0][2, 3]
    for i in range(n_images):
        min_x = min(min_x, pose_all[i][0, 3])
        max_x = max(max_x, pose_all[i][0, 3])
        min_y = min(min_y, pose_all[i][1, 3])
        max_y = max(max_y, pose_all[i][1, 3])
        min_z = min(min_z, pose_all[i][2, 3])
        max_z = max(max_z, pose_all[i][2, 3])
    print(f"[{min_x}, {max_x}]")
    print(f"[{min_y}, {max_y}]")
    print(f"[{min_z}, {max_z}]")

    visualizer = CameraPoseVisualizer([-2, 2], [-2, 2], [-2, 2])
    for i in range(n_images):
        visualizer.extrinsic2pyramid(pose_all[i], focal_len_scaled=0.25, aspect_ratio=0.3)
    # visualizer.show()

def load_pickle(path):
    """
    打印pkl格式文件（类似一个table）
    :param path: # e.g. pkl_path = './out/demo_matterport/generation/time_generation_full.pkl'
    :return:
    """
    f = open(path,'rb')
    data = pickle.load(f)
    print(data)

if (__name__=="__main__"):
    npz_path = "data/public_data/bmvs_dog/preprocessed/cameras_sphere.npz"
    # load_npz(npz_path)
    render_camera_params(npz_path)