from InstructionMemory.InstructionBlock import InstructionBlock

# Direccion inicial de la memoria de instrucciones
INITIAL_DIR = 384


# Clase para la memoria de instrucciones
class InstructionMemory:

    # Constructor que inicializa la lista con los valores
    def __init__(self):
        self.__instruction_block_array = []
        self.__next_word = 0
        self.__block_amount = 0

    # Método para cargar todos los bloques de instrucciones de la memoria principal
    # Recibe la instruccion a insertar
    def store_instruction(self, instruction):
        # Se calcula el numero de bloque
        block_number = self.__next_word // 16

        # Caso en el que es la primera instrucion
        if len(self.__instruction_block_array) == 0:
            # Se crea un nuevo bloque y se agrega
            instruction_block = InstructionBlock()
            self.__instruction_block_array.append(instruction_block)

        if block_number == self.__block_amount:
            self.__instruction_block_array[block_number].insert_instruction(instruction)
        else:
            # Se crea un nuevo bloque y se agrega
            instruction_block = InstructionBlock()
            instruction_block.insert_instruction(instruction)
            self.__instruction_block_array.append(instruction_block)
            # Se incrementa la cantidad de bloques
            self.__block_amount += 1

        # Se incrementa en 4 para la siguiente instruccion
        self.__next_word += 4

    # Funcion para retornar el bloque del pc correspondiente
    def get_instruction_block(self, pc):
        # Se adapta el PC para utilizarlo en esta funcion
        pc_function = pc - INITIAL_DIR

        # Se revisa que el pc recibido sea multiplo de 4
        if pc_function % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        # Se revisa que el bloque exista
        if pc_function >= self.__next_word:
            raise TypeError("Se solicito una instruccion que no existe, direccion: " + str(pc))
        # Se revisa que sea mayor igual a 0
        if pc_function < 0:
            raise TypeError("El PC solicitado no corresponde a una direccion de la memoria de instrucciones")
        # Se retorna el bloque
        return self.__instruction_block_array[pc_function // 16]

    # Funcion para obtener la instruccion especifica
    def get_instruction(self, pc):
        # Se adapta el PC para utilizarlo en esta funcion
        pc_function = pc - INITIAL_DIR

        # Se revisa que el pc recibido sea multiplo de 4
        if pc_function % 4 != 0:
            raise TypeError("Se recibio un PC que no es multiplo de 4")
        # Se revisa que el bloque exista
        if pc_function >= self.__next_word:
            raise TypeError("Se solicito una instruccion que no existe, direccion: " + str(pc))
        # Se revisa que sea mayor igual a 0
        if pc_function < 0:
            raise TypeError("El PC solicitado no corresponde a una direccion de la memoria de instrucciones")
        # Se retorna la instruccion
        return self.__instruction_block_array[pc_function // 16].get_instruction(pc)

    # Funcion para imprimir el bloque
    def print_instruction_block(self, index):
        self.__instruction_block_array[index].print_block()
