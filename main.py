from MainMemory import MainMemory
from PCBDataStructure import PCBDataStructure


def main():
    # Pruebas
    pcb = PCBDataStructure()
    system_main_memory = MainMemory(pcb)
    system_main_memory.print_instruction_block(1)




main()

