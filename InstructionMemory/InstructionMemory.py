from InstructionMemory.InstructionBlock import InstructionBlock


# Clase para la memoria de instrucciones
class InstructionMemory:

    # Constructor que inicializa la lista con los valores
    def __init__(self):
        self.__instruction_block_array = []

    # Método para cargar todos los bloques de instrucciones de la memoria principal
    # Recibe el arreglo con todas las instrucciones, que también son arreglos de tamaño 4
    def store_instructions(self, all_instruction_array):
        block_counter = 0
        # Se itera sobre el array de instrucciones recibido,
        # Iteración por bloques
        while block_counter*4 < len(all_instruction_array):
            instruction_block = InstructionBlock()
            iterator = block_counter*4
            instructions_array = []
            # Iteración por instrucciones dentro del bloque
            while iterator < len(all_instruction_array) and iterator < (block_counter*4+4):
                instructions_array.append(all_instruction_array[iterator])
                iterator += 1
            instruction_block.initialize_instructions(instructions_array)
            self.__instruction_block_array.append(instruction_block)
            block_counter += 1

    # Función para imprimir el bloque
    def print_instruction_block(self, index):
        self.__instruction_block_array[index].print_block()
