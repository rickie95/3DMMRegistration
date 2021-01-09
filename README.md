<p align="center">3DMMRegistration was helpful to you? Feel free to contribute or <a href="https://www.buymeacoffee.com/rickie95" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="35" style="max-width:100%;vertical-align: middle;"></a></p>

# Shape Registrator

*A tool for 3D face models aligment. With a GUI.*

![Application screenshot](https://github.com/rickie95/3DMMRegistration/blob/master/resources/gitScreen1.png)

Shape Registrator works with 3D model and supports **.mat** (Matlab), **.wrl** (WRML) and **.off** (Open File Format) file formats.

## 2019 Update:
- Displacement map can now be saved as a Pickle file.
- Target model can be rotated, in order to provide a good starting point for CPD algorithm.
- Source model is now shown in the target section while registrated.

### Installation

1. Clone repo.
2. `pip install -r requirements.txt`
3. Run main.py

### Usage

1. Load two models, you can choose between .mat, .wrl + .bnd and .off formats.
2. Select the amount of points to be used and the CPD version: rigid, affine or deformable.
3. "Registrate", and wait for the result.

In the log box you can see the registration error and some messages.

### About file formats:

**.mat** files have to contain a '3ddata' field storing 3D points coordinates (a Nx3 matrix) and a 'landmarks3d' witch stores the landmarks coordinates (Nx3 matrix).

**.wrl** files should be paired with a .bnd file storing the landmarks coordinates. If a .png image with the same name is aviable, it will be used for the background of the plot tool.

**.off** files must contain 3D points coordinates, faces are not mandatory and will be ignored.

## Insights

In the very heart of the application there's the *Coherent Point Drift* algorithm[1], witch allows to registrate two point sets regardless from the transformation's nature.
In fact, CPD provides three kind of transformation: **rigid**, **affine** and **deformable**; with crescent grades of freedom.

It's possible to control the quantity of the points involved in the registration process: you can choose to keep all of them (100%) or to reduce until 30% of original number. The sampling policy used is *uniform and casual*.

Reduce the amount of points makes  the registration process faster, but - only for affine and deformable case - the transformation matrices can't be used to process the entire point set. However, we can take advantage of this option in the rigid case.

## Packages required
*A requirements.txt is provided, in order to be used with pip*

Package | Version
--------|--------
numpy   | >=1.15.0
scipy   | >=1.3
matplotlib| ~2.2.3
PyQt5| ~5.11.2
h5py| ~2.8
pycpd| ~1.0.3

The application was tested so far with Python 3.7 x64 operating on Windows 10 and Ubuntu 16.04 LTS. Should work on MacOs as well, since PyQt5 is cross-platform.

## References
[1] Andriy Myronenko and Xubo Song, "*Point Set Registration: Coherent Point Drift*",  IEEE Trans. on Pattern Analysis and Machine Intelligence, vol. 32, issue 12, pp. 2262-2275, 15 May 2009 {[link](https://arxiv.org/pdf/0905.2635.pdf)}

[2] Alessandro Soci and Gabriele Barlacchi, [AlessandroSoci/3DMM-Facial-Expression-from-Webcam](https://github.com/AlessandroSoci/3DMM-Facial-Expression-from-Webcam)

[3] Alessandro Sestini and Francesco Lombardi, [fralomba/Facial-Expression-Prediction](https://github.com/fralomba/Facial-Expression-Prediction)
