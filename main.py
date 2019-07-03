from CPU import CPU
from SimulationStatistics import SimulationStatistics

simulation_statistics = SimulationStatistics()
def main(simulation_statistics):
    # Pruebas
    # pcb = PCBDataStructure()
    # system_main_memory = MainMemory(pcb)
    # pcb.print_all_pcbs()
    # system_main_memory.print_instruction_block(0)
    # print("")
    # block = system_main_memory.get_instruction_block(384)
    # block.print_block()
    # print("")
    # instruction = system_main_memory.get_instruction(668)
    # instruction.print_instruction()
    cpu = CPU(simulation_statistics)
    cpu.start_cores()
    # simulation_statistics.printStatistics()


main(simulation_statistics)
# simulation_statistics.printStatistics()
