import numpy as np


def loadWRML(path):
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

    file = loadFile(path)
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

def loadBND(path):
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

    file = loadFile(path)
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


def loadFile(path):
    try:
        file = open(path, "r")
    except FileNotFoundError as ex:
        print("Can't find the file")
        return None
    except FileExistsError as ex:
        print("File exists but got troubles")
        return None
    except Exception as ex:
        print("Somthing gone wrong")
        return None

    return file

pp = loadBND("F0001_NE00WH_F3D.bnd")
print("done")