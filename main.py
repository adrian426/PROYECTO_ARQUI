from MainMemory import MainMemory
from PCBDataStructure import PCBDataStructure


def main():
    # Pruebas
    pcb = PCBDataStructure()
    system_main_memory = MainMemory(pcb)
    pcb.print_all_pcbs()
    # system_main_memory.print_instruction_block(0)
    # print("")
    # block = system_main_memory.get_instruction_block(384)
    # block.print_block()
    # print("")
    # instruction = system_main_memory.get_instruction(668)
    # instruction.print_instruction()


main()
