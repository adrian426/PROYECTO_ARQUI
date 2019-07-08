import os
import os.path as path


class FileReader:

    def __init__(self, hilillos_to_run):
        # Set hilillos path
        if hilillos_to_run == 0:
            self.hilillos_path = path.join(".", "Hilillos/Hilillo-FACILISIMO")
        elif hilillos_to_run == 1:
            self.hilillos_path = path.join(".", "Hilillos/Hilillos-SIMPLES")
        elif hilillos_to_run == 2:
            self.hilillos_path = path.join(".", "Hilillos/HilillosPruebaFinal")

    # Method to obtain all file names on the hilillos path
    def get_hilillos_files_list(self):
        hilillos = os.listdir(self.hilillos_path)
        hilillos_array = []
        for hilillo in hilillos:
            if hilillo.endswith(".txt"):
                hilillos_array.append(hilillo)
        return hilillos_array


    # Method to read a file and obtain all the instructions
    def read_hilillos(self, file_name):
        file_path = path.join(self.hilillos_path, file_name)
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
