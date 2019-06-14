def read_hilillos(file_name):
    file = open(file_name, "r")
    instruction_array = []
    for line in file:
        instruction = line.split()
        instruction_array.append(instruction)
    return instruction_array