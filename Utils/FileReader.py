import os

# Direccion del directorio con los hilillos
HILILLOS_PATH = r'.\Hilillos'


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
    file = open(HILILLOS_PATH + "\\" + file_name, "r")
    instruction_array = []
    for line in file:
        instruction = line.split()
        instruction_array.append(instruction)
    file.close()
    return instruction_array
