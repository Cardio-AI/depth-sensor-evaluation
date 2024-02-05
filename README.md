# Depth-camera evaluation

This repository contains code designed to facilitate the evaluation of depth-related metrics for [Intel RealSense](https://www.intelrealsense.com/) stereo cameras and [Stereolabs](https://www.stereolabs.com/) ZED cameras. These metrics are crucial for assessing the accuracy and performance of stereo camera systems in tasks such as 3D reconstruction, object detection, and depth estimation.
This repository was used for the following paper: Comparative evaluation of three commercially available markerless depth sensors for close-range use in surgical simulation.

For a more detailed description, including evaluation setup and additional results, we refer you to our associated [paper](https://doi.org/10.1007/s11548-023-02887-1).

## Abstract

**Purpose**
Minimally invasive surgeries have restricted surgical ports, demanding a high skill level from the surgeon. 
Surgical simulation potentially reduces this steep learning curve and additionally provides quantitative feedback. 
Markerless depth sensors show great promise for quantification, but most such sensors are not designed for accurate reconstruction of complex anatomical forms in close-range.

**Methods** 
This work compares three commercially available depth sensors, namely the Intel $D405$, $D415$, and the Stereolabs *Zed-Mini* in the range of $12$ to $20\mathrm{cm}$, for use in surgical simulation. 
Three environments are designed that closely mimic surgical simulation, comprising planar surfaces, rigid objects, and mitral valve models of silicone and realistic porcine tissue.
The cameras are evaluated on $Z$-accuracy, temporal noise, fill rate, checker distance, point cloud comparisons, and visual inspection of surgical scenes, across several camera settings.

**Results** The Intel cameras show sub-mm accuracy in most static environments.
The $D415$ fails in reconstructing valve models, while the Zed-Mini provides lesser temporal noise and higher fill rate. The $D405$ could reconstruct anatomical structures like the mitral valve leaflet and a ring prosthesis, but performs poorly for reflective surfaces like surgical tools and thin structures like sutures. 

**Conclusion** If a high temporal resolution is needed and lower spatial resolution is acceptable, the Zed-Mini is the best choice, whereas the Intel $D405$ is the most suited for close-range applications. The $D405$ shows potential for applications like deformable registration of surfaces, but is not yet suitable for applications like real-time tool tracking or surgical skill assessment.

## Project-Organization

    ├── LICENSE
    ├── README.md               <- The top-level README for developers using this project.
    ├── src                     <- Source code of the project.
    │   ├── notebooks           <- Example Jupyter notebooks how to use the metrics and data loading functions.
    │   ├── inout               <- Helper function to read and load images and depth values from .bag and .svo files
    │   └── metrics             <- Metrics definitions


## Citation
```BibTeX
@article{Burger2023,
  title = {Comparative evaluation of three commercially available markerless depth sensors for close-range use in surgical simulation},
  volume = {18},
  ISSN = {1861-6429},
  url = {http://dx.doi.org/10.1007/s11548-023-02887-1},
  DOI = {10.1007/s11548-023-02887-1},
  number = {6},
  journal = {International Journal of Computer Assisted Radiology and Surgery},
  publisher = {Springer Science and Business Media LLC},
  author = {Burger,  Lukas and Sharan,  Lalith and Karl,  Roger and Wang,  Christina and Karck,  Matthias and De Simone,  Raffaele and Wolf,  Ivo and Romano,  Gabriele and Engelhardt,  Sandy},
  year = {2023},
  month = may,
  pages = {1109–1118}
}
```