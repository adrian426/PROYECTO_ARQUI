from InstructionMemory.InstructionMemory import InstructionMemory
from DataMemory.DataMemory import DataMemory
from PCB import PCB
from Utils.FileReader import get_hilillos_files_list, read_hilillos

# Direccion inicial de la memoria de instrucciones
INITIAL_DIR = 384


# Clase para la memoria principal del sistema
class MainMemory:

    # Constructor
    def __init__(self, pcb_structure):

        self.__data_memory = DataMemory()
        self.__instruction_memory = InstructionMemory()

        self.__data_memory.initialize_memory()

        # Obtiene los nombres de los hilillos
        hilillos_names = get_hilillos_files_list()

        # Contador de direcciones de memoria
        instruction_counter = INITIAL_DIR

        # Crea el arreglo de hilillos e inicializa la memoria de instrucciones
        for hilillo in hilillos_names:
            instructions_hilillo = read_hilillos(hilillo)

            # Inicializa la memoria de instrucciones
            bytes_added = 0
            for instruction in instructions_hilillo:
                self.__instruction_memory.store_instruction(instruction)
                bytes_added += 4

            # Se crea el PCB y se inserta en la estructura del PCB
            register_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            instruction_pcb = PCB(hilillo, instruction_counter, register_array)

            # Se inserta el PCB en la estructura
            pcb_structure.queuePCB(instruction_pcb)

            # Se incrementa el contador de instruccion
            instruction_counter += bytes_added

    # Metodo para obtener una instruccion de la memoria de instrucciones dado un PC
    def get_instruction_block(self, pc):
        # Se revisa que el PC sea multiplo de 4
        if pc % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        else:
            return self.__instruction_memory.get_instruction_block(pc)

    # Metodo para obtener una instruccion especifica
    def get_instruction(self, pc):
        # Se revisa que el PC sea multiplo de 4
        if pc % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        else:
            return self.__instruction_memory.get_instruction(pc)

    # Metodo de prueba
    def print_instruction_block(self, block_id):
        self.__instruction_memory.print_instruction_block(block_id)

    #Method to get data block from data memory
    def get_data_block(self, mem_add):
        return self.get_data_block(mem_add)

    def set_data_block(self, mem_add, data_block):
        self.__data_memory.store_memory_block(mem_add, data_block)