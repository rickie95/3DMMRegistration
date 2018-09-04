# Shape Registrator

*A tool for 3D face models aligment. With a GUI.*

![Application screenshot](/resources/screenGit1.png)

Shape Registrator works with 3D model and supports **.mat** (Matlab) and **.wrl** (WRML) file formats.

### Installation

1. Clone repo.
2. `pip install requirements.txt`
3. Run main.py

### Usage

1. Load two models, you can choose between .mat and .wrl + .bnd formats.
2. Select the amount of points to be used.
3. "Registrate", and wait for the result.

In the log box you can see the registration error and some messages.

### About file formats:

**.mat** files have to contain a '3ddata' field storing 3D points coordinates (a Nx3 matrix) and a 'landmarks3d' witch stores the landmarks coordinates (Nx3 matrix).

**.wrl** files should be paired with a .bnd file storing the landmarks coordinates. If a .png image with the same name is aviable, it will be used for the background of the plot tool.

## Insights

In the very heart of the application there's the *Coherent Point Drift* algorithm[1], witch allows to registrate two point sets regardless from the transformation's nature.
In fact, CPD provides three kind of transformation: **rigid**, **affine** and **deformable**; with crescent grades of freedom.

It's possible to control the quantity of the points involved in the registration process: you can choose to keep all of them (100%) or to reduce until 30% of original number. The sampling policy used is *uniform and casual*.

Reduce the amount of points makes  the registration process faster, but - only for affine and deformable case - the transformation matrices can't be used to process the entire point set. However, we can take advantage of this option in the rigid case.

## Packages required
*A requirements.txt is provided, in order to be used with pip*

Package | Version
--------|--------
numpy   | ~1.15.0
scipy   | ~1.1
matplotlib| ~2.2.3
PyQt5| ~5.11.2
h5py| ~2.8
pycpd| ~1.0.3

The application was tested so far with Python 3.7 x64 operating on Windows 10. Should work on Linux as well, the PyQt5 GUI should be cross-platform.

## References
[1] Andriy Myronenko and Xubo Song, "*Point Set Registration: Coherent Point Drift*",  IEEE Trans. on Pattern Analysis and Machine Intelligence, vol. 32, issue 12, pp. 2262-2275, 15 May 2009 {[link](https://arxiv.org/pdf/0905.2635.pdf)}

[2] Alessandro Soci and Gabriele Barlacchi, [AlessandroSoci/3DMM-Facial-Expression-from-Webcam](https://github.com/AlessandroSoci/3DMM-Facial-Expression-from-Webcam)

[3] Alessandro Sestini and Francesco Lombardi, "*Studio e predizione di espressioni facciali per modelli 3D*"
