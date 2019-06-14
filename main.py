import MainMemory as MainMemory
import PCBDataStructure as PCBDataStructure

def main():
    # Pruebas
    pcb = PCBDataStructure()
    system_main_memory = MainMemory(pcb)
    system_main_memory.print_instruction_block(1)

main()

