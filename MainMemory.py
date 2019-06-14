from InstructionMemory.InstructionMemory import InstructionMemory
import PCB


# Clase para la memoria principal del sistema
class MainMemory:

    # Constructor
    def __init__(self, PCBStructure):
        # Declara la memoria de instrucciones
        self.__instruction_memory = InstructionMemory()
        self.__hilillo_id = 0
        # Inicializa la memoria de instrucciones
        # Por ahora se utiliza este hilillo de prueba
        # ToDo: Agregar lectura del archivo
        hilillo1 = [[19, 20, 0, 2],
                    [19, 3, 0, 5],
                    [19, 8, 0, 8],
                    [19, 4, 0, 200],
                    [37, 4, 20, 0],
                    [37, 4, 20, 4],
                    [37, 4, 20, 8],
                    [37, 4, 20, 12],
                    [37, 0, 0, 176],
                    [999, 0, 0, 0]]

        hilillo2 = [[19, 20, 0, 2],
                    [19, 3, 0, 5],
                    [19, 8, 0, 8],
                    [19, 4, 0, 200],
                    [37, 4, 20, 0],
                    [37, 4, 20, 4],
                    [37, 4, 20, 8]]

        array_hilillos = [hilillo1, hilillo2]



        for hilillo in array_hilillos:
            instruction_counter = 0
            bytes_added = 0
            for instruction in hilillo:
                self.__instruction_memory.store_instruction(instruction)
                bytes_added += 1
            # Se crea el PCB y se inserta en la estructura del PCB
            register_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            instruction_pcb = PCB(self.__hilillo_id, instruction_counter, register_array)

            # Se inserta el PCB en la estructura
            PCBStructure.queuePCB(instruction_pcb)

            # Se incrementa el contador de instruccion
            instruction_counter += bytes_added






    # Metodo de prueba
    def print_instruction_block(self, block_id):
        self.__instruction_memory.print_instruction_block(block_id)
