from DataMemory.DataBlock import DataBlock
from StatesEnum import StatesEnum

DATA_BUS_OPERATION_CLOCK_CYCLES = 32
CONSULT_OTHER_CACHE_CLOCK_CYCLES = 2
LOCK_ERROR = -1


# Class to execute the LR instruction
class LR:

    def __init__(self, core_instance):
        self.__core_instance = core_instance

    def execute(self, instruction):
        while self.exec_load(instruction) == LOCK_ERROR:
            self.__core_instance.release_all_locks_acquired()
            self.__core_instance.set_instruction_system_clock_cycles(1)

    # Start the instruction execution
    # Receives the instruction to execute
    # Returns the execution cycles of the instruction, -1 if the execute cant get the locks
    def exec_load(self, instruction):

        # Set the values for the execution
        destination_registry = instruction.get_instruction()[1]
        direction_registry = instruction.get_instruction()[2]
        total_execution_clock_cycles = 0

        # Calculate the direction of the memory address on memory
        memory_address_to_get = \
            self.__core_instance.get_register_value(direction_registry)

        #if int(memory_address_to_get/16) == 16:
        print(""+str(memory_address_to_get))

        # Check if there is a cache miss
        # LOCK SELF CACHE!!
        if self.__core_instance.acquire_self_cache():
            # Get self cache
            mem_address_on_cache = self.__core_instance.get_if_mem_address_is_on_self_cache(memory_address_to_get)
            if mem_address_on_cache:
                mem_address_block_invalid = \
                    self.__core_instance.get_memory_address_state_on_cache(memory_address_to_get) == StatesEnum.INVALID
                if mem_address_block_invalid:
                    # Invalid on self cache
                    cache_miss_cycles_result = self.solve_cache_miss(memory_address_to_get)
                    if cache_miss_cycles_result == LOCK_ERROR:
                        return LOCK_ERROR
                    else:
                        total_execution_clock_cycles += cache_miss_cycles_result
                        self.__core_instance.increase_cache_miss()
            else:
                # Not on self cache
                cache_miss_cycles_result = self.solve_cache_miss(memory_address_to_get)
                if cache_miss_cycles_result == LOCK_ERROR:
                    return LOCK_ERROR
                else:
                    total_execution_clock_cycles += cache_miss_cycles_result
                    self.__core_instance.increase_cache_miss()
        else:
            # Can't get self cache
            return LOCK_ERROR

        # Load the value in the register
        self.__core_instance.set_register(destination_registry,
                                          self.__core_instance.get_data_cache_value(memory_address_to_get))

        # Set the RL value
        self.__core_instance.set_self_rl(memory_address_to_get)

        # Returns the execution time
        self.__core_instance.set_instruction_system_clock_cycles(total_execution_clock_cycles)
        return total_execution_clock_cycles

    # Method to solve cache miss
    def solve_cache_miss(self, m_address):
        clock_cycles = 0
        # LOCK OTHER CORE CACHE AND DATA BUS
        if self.__core_instance.acquire_other_and_data_bus_locks():
            # LOCKS ACQUIRED + 2 Other cache +32 Data bus
            clock_cycles += CONSULT_OTHER_CACHE_CLOCK_CYCLES + DATA_BUS_OPERATION_CLOCK_CYCLES
            if self.__core_instance.get_if_memory_address_on_other_cache(m_address):
                # Memory address is on the other core cache
                if self.__core_instance.get_memory_address_state_on_other_cache(
                        m_address) == StatesEnum.MODIFIED:
                    # Other core cache block is modified
                    # Store the other core block and get the new block
                    data_block_to_insert = DataBlock(0)
                    data_block_to_insert.copy_data_block(
                        self.__core_instance.store_other_core_data_cache_block_on_main_memory(
                            m_address, StatesEnum.SHARED))
                    clock_cycles += self.__core_instance.store_block_on_self_cache(
                        StatesEnum.SHARED, m_address, data_block_to_insert)
                    return clock_cycles
            # Memory address isn't in the other core or isn't modified
            # LOCK RELEASED OTHER CORE CACHE
            self.__core_instance.release_other_core_cache()
            # Only need to load to self cache + 32
            main_memory_data_block = self.__core_instance.get_data_block(m_address)
            data_to_insert = DataBlock(0)
            data_to_insert.copy_data_block(main_memory_data_block)
            clock_cycles += self.__core_instance.store_block_on_self_cache(StatesEnum.SHARED, m_address, data_to_insert)
            return clock_cycles
        else:
            # Cant get the other core cache
            return LOCK_ERROR


