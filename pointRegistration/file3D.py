from graphicInterface.console import Logger
import numpy as np
import os
import h5py


def load_wrml(path):
    """
    Restituisce un array Nx3 con le coordinate 3D dei punti contenuti in un file .wrl.

    Attenzione, il file deve avere questa precisa struttura:
    **** roba*****
    *************
            point [
                x.xxx y.yyyyyy z.zzzzz,
                x.xxx y.yyyyyy z.zzzzz,
                ****
                ****
                ****
                x.xxx y.yyyyyy z.zzzzz,
                x.xxx y.yyyyyy z.zzzzz
                ]
    ****** roba ******
    ******************

    Notare che manca l'ultima virgola

    Ai fini del caricamento il resto del contenuto non è importante, ma essendo questo
    un parser a riga robusto come un bicchiere di cristallo è consigliabile assicurarsi
    che il ile rispetti la struttura descritta prima di dare colpa all'implementazione
    da veri n00b.

    :param path: pathname del file (" pippo.wrl")
    :return:    un array numpy Nx3, dove N è il numero dei punti contenuti nel file
    """

    file = load_file(path)
    if file is None:
        return None

    while file.readline().strip() != "point [":
        pass

    # arrivo alla prima riga dei punti
    points_num = 0
    points = np.empty((1000, 3))
    line = file.readline().strip()
    while line.strip() != "]":
        x, y, z = line[0:len(line)-1].split(" ")
        points[points_num] = [float(x), float(y), float(z)]
        points_num +=1
        if points_num == points.size/3:
            points = np.concatenate([points, np.empty((1000, 3))])
        line = file.readline().strip()
    return points[0:points_num, :]


def load_bnd(path):
    """
    Restituisce un array Nx3 con le coordinate 3D dei landmarks contenuti in un file .bnd.

    Attenzione, il file deve avere questa precisa struttura:
    nnnn x.xxx y.yyyyyy z.zzzzz
    nnnn x.xxx y.yyyyyy z.zzzzz
    nnnn x.xxx y.yyyyyy z.zzzzz
    *******
    *******
    *******
    nnnn x.xxx y.yyyyyy z.zzzzz
    nnnn x.xxx y.yyyyyy z.zzzzz

    Ai fini del caricamento il resto del contenuto non è importante, ma essendo questo
    un parser a riga robusto come un bicchiere di cristallo è consigliabile assicurarsi
    che il ile rispetti la struttura descritta prima di dare colpa all'implementazione
    da veri n00b.

    :param path: pathname del file (" pippo.wrl")
    :return:    un array numpy Nx3, dove N è il numero dei punti contenuti nel file
    """

    file = load_file(path)
    if file is None:
        return None

    # arrivo alla prima riga dei punti
    points_num = 0
    points = np.empty((10, 3))
    line = file.readline().strip()
    line = line.replace("\t\t", " ")
    while line.strip() != "":
        nn, x, y, z = line.split(" ")
        points[points_num] = [float(x), float(y), float(z)]
        points_num += 1
        if points_num == points.size/3:
            points = np.concatenate([points, np.empty((10, 3))])
        line = file.readline().replace("\t\t", " ").strip()
    return points[0:points_num, :]


def load_off(file, faces_required=False):
    """
    Reads vertices and faces from an off file.

    :param file: path to file to read
    :type file: str
    :param faces_required: True if the function should return faces also
    :type: bool
    :return: vertices and faces as lists of tuples
    :rtype: [(float)], [(int)]
    """

    assert os.path.exists(file)

    with open(file, 'r') as fp:
        lines = fp.readlines()
        lines = [line.strip() for line in lines]

        assert (lines[0] == 'OFF'), "Invalid preambole"

        parts = lines[1].split(' ')
        assert (len(parts) == 3), "Need exactly 3 parameters on 2nd line (n_vertices, n_faces, n_edges)."

        num_vertices = int(parts[0])
        assert num_vertices > 0

        num_faces = int(parts[1])
        if faces_required:
            assert num_faces > 0

        vertices = []
        for i in range(num_vertices):
            vertex = lines[2 + i].split(' ')
            vertex = [float(point) for point in vertex]
            assert (len(vertex) == 3), str("Invalid vertex row on line " + str(i))

            vertices.append(vertex)

        if num_vertices > len(vertices):
            row = "WARNING: some vertices were not loaded correctly: {0} declared vs {1} loaded."
            Logger.addRow(row.format(num_vertices, len(vertices)))

        vertices = np.asarray(vertices)

        if faces_required:
            faces = []
            for i in range(num_faces):
                face = lines[2 + num_vertices + i].split(' ')
                face = [int(index) for index in face]

                assert face[0] == len(face) - 1
                for index in face:
                    assert 0 <= index < num_vertices

                assert len(face) > 1

                faces.append(face)
            return vertices, faces

        return vertices


def load_file(path):
    try:
        file = open(path, "r")
    except FileNotFoundError as ex:
        print("Can't find the file")
        return None
    except FileExistsError as ex:
        print("File exists but got troubles")
        return None
    except Exception as ex:
        print("Something gone wrong")
        return None

    return file


def save_file(filepath, model):
    filename, file_extension = os.path.splitext(filepath)

    if file_extension == '.off':
        save_off(filepath, model)
    if file_extension == '.wrl':
        save_wrl(filepath, model)
    if file_extension == '.mat':
        save_mat(filepath, model)


def save_off(filepath, model):
    with open(filepath, "w") as file:
        file.write("OFF\n")
        n_points = int(model["model_data"].size / 3)
        file.write(str(n_points) + " 0 0\n")
        row = "{0} {1} {2}\n"
        for index in range(n_points):
            x, y, z = model["model_data"][index]
            file.write(row.format(x, y, z))
        file.close()


def save_mat(filepath, model):
    f = h5py.File(filepath, "w")
    for key, value in model.items():
        f.create_dataset(key, data=value)
    f.close()


def save_wrl(filepath, model):
    pass