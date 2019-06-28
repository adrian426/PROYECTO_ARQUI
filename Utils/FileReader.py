import os
import os.path as path


# Direccion del directorio con los hilillos
HILILLOS_PATH = path.join(".", "HilillosDificiles")


# Metodo para obtener los archivos de texto en el directorio
def get_hilillos_files_list():
    hilillos = os.listdir(HILILLOS_PATH)
    hilillos_array = []
    for hilillo in hilillos:
        if hilillo.endswith(".txt"):
            hilillos_array.append(hilillo)
    return hilillos_array


# Metodo para leer un archivo y obtener el arreglo de instrucciones
def read_hilillos(file_name):
    file_path = path.join(HILILLOS_PATH, file_name)
    file = open(file_path, "r")
    instruction_array = []
    instruction_int = []
    for line in file:
        instruction = line.split()
        for inst in instruction:
            instruction_int.append(int(inst))
        instruction_array.append(instruction_int)
        instruction_int = []
    file.close()
    return instruction_array
