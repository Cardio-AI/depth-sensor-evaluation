import cloudComPy as cc
import numpy as np
import psutil
import os

os.environ["_CCTRACE_"]="ON"                                           # only if you want debug traces from C++

def compute_c2c(source_cloud,target_cloud,scale=1000.):
    #check if the point cloud are valid
    if source_cloud is None or target_cloud is None:
        return None,None
    # cloud
    dist_tool = cc.DistanceComputationTools

    # h_approx_dist = dist_tool.computeApproxCloud2CloudDistance(source_cloud,target_cloud)

    nbCpu = psutil.cpu_count()
    max_search = 8
    bestOctreeLevel = cc.DistanceComputationTools.determineBestOctreeLevel(target_cloud,None,source_cloud,maxSearchDist=max_search)
    params = cc.Cloud2CloudDistancesComputationParams()
    params.maxThreadCount = nbCpu
    params.octreeLevel = bestOctreeLevel
    # model: 'LS', 'NO_MODEL', 'QUADRIC', 'TRI'
    params.localModel = cc.LOCAL_MODEL_TYPES.QUADRIC
    params.kNNForLocalModel = 6
    params.maxSearchDist = max_search


    h_dist = dist_tool.computeCloud2CloudDistances(target_cloud,source_cloud,params)
    if h_dist < 0:
        return None, None

    # calc min/max/mean/var
    sf = target_cloud.getScalarField(target_cloud.getNumberOfScalarFields()-1)
    sf.computeMinAndMax()
    sf_min,sf_max = sf.getMin(),sf.getMax()
    mean,var = sf.computeMeanAndVariance()
    std = np.sqrt(var)

    return mean*scale,std*scale

def compute_c2m(source_cloud,target_mesh,scale=1000.):
    #check if the point cloud are valid
    if source_cloud is None or target_mesh is None:
        return None,None
    dist_tool = cc.DistanceComputationTools

    # mesh
    # c2m_approx_dist = dist_tool.computeApproxCloud2MeshDistance(source_cloud,target_mesh)

    nbCpu = psutil.cpu_count()
    max_search = 8
    bestOctreeLevel_mesh = cc.DistanceComputationTools.determineBestOctreeLevel(source_cloud,target_mesh,None,maxSearchDist=max_search)
    mesh_params = cc.Cloud2MeshDistancesComputationParams()
    mesh_params.maxThreadCount = nbCpu
    mesh_params.octreeLevel = bestOctreeLevel_mesh
    mesh_params.maxSearchDist = max_search


    h_dist = dist_tool.computeCloud2MeshDistances(source_cloud,target_mesh,mesh_params)
    if h_dist < 0:
        return None, None

    # calc min/max/mean/var
    sf_mesh = source_cloud.getScalarField(source_cloud.getNumberOfScalarFields()-1)
    sf_mesh.computeMinAndMax()
    sfMesh_min,sfMesh_max = sf_mesh.getMin(),sf_mesh.getMax()
    mesh_mean,mesh_var = sf_mesh.computeMeanAndVariance()
    mesh_std = np.sqrt(mesh_var)

    return mesh_mean*scale, mesh_std*scale
