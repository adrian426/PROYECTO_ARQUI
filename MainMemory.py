from InstructionMemory import InstructionMemory


# Clase para la memoria principal del sistema
class MainMemory:

    # Constructor
    def __init__(self):
        # Declara la memoria de instrucciones
        self.__instruction_memory = InstructionMemory()
        # Inicializa la memoria de instrucciones
        # Por ahora se utiliza este hilillo de prueba
        # ToDo: Agregar lectura del archivo
        self.__instruction_memory.store_instructions([[19, 20, 0, 2],
                                                     [19, 3, 0, 5],
                                                     [19, 8, 0, 8],
                                                     [19, 4, 0, 200],
                                                     [37, 4, 20, 0],
                                                     [37, 4, 20, 4],
                                                     [37, 4, 20, 8],
                                                     [37, 4, 20, 12],
                                                     [37, 0, 0, 176],
                                                     [999, 0, 0, 0]])

        # Se crea el PCB y se inserta en la estructura del PCB
        # register_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # instruction_pcb = PCB()

    # Metodo de prueba
    def print_instruction_block(self, block_id):
        self.__instruction_memory.print_instruction_block(block_id)
