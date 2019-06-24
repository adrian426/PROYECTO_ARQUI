from StatesEnum import StatesEnum
from DataMemory.DataBlock import DataBlock


DATA_BUS_OPERATION_CLOCK_CYCLES = 32
CONSULT_OTHER_CACHE_CLOCK_CYCLES = 2
LOCK_ERROR = -1


# Class to execute the SC instruction
class SC:

    def __init__(self, core_instance):
        self.__core_instance = core_instance

    # Start the instruction execution
    # Receives the core instance, and the instruction to execute
    # Returns the execution cycles of the instruction, -1 if the execute cant get the locks
    def execute(self, instruction):

        # Set the values for the execution
        source_registry = instruction.get_instruction()[2]
        direction_registry = instruction.get_instruction()[1]
        total_execution_clock_cycles = 0

        # Calculate the direction of the memory address on memory
        mem_add_to_store = \
            self.__core_instance.get_register_value(direction_registry)

        # Check if there is a cache miss
        # LOCK SELF CACHE!!
        if self.__core_instance.acquire_self_cache():
            # Get self cache
            mem_address_on_cache = self.__core_instance.get_if_mem_address_is_on_self_cache(mem_add_to_store)
            mem_address_state_on_cache = self.__core_instance.get_memory_address_state_on_cache(mem_add_to_store)
            # Check if the block is shared and the RL value is the needed
            if mem_address_on_cache and mem_address_state_on_cache == StatesEnum.SHARED and \
                    (self.__core_instance.get_self_rl == mem_add_to_store):
                # SHARED ON SELF CACHE, CHECK THE OTHER CORE
                # LOCK OTHER CORE CACHE AND DATA BUS
                if self.__core_instance.acquire_other_and_data_bus_locks():
                    # Get if the block is on the other core and get the state
                    mem_address_on_other_core = \
                        self.__core_instance.get_if_memory_address_on_other_cache(mem_add_to_store)
                    mem_address_state_on_other_cache = self.__core_instance.get_memory_address_state_on_other_cache(
                        mem_add_to_store)
                    # Clock cycles consult other core cache
                    total_execution_clock_cycles += CONSULT_OTHER_CACHE_CLOCK_CYCLES
                    if mem_address_on_other_core and mem_address_state_on_other_cache == StatesEnum.SHARED:
                        # The block is shared on the other core
                        self.__core_instance.change_block_state_on_other_core_cache(
                            mem_add_to_store, StatesEnum.INVALID)
                        # Invalidate the RL on the other core, in the case that it was using a lr
                        self.__core_instance.invalidate_other_core_rl(mem_add_to_store)
                    else:
                        # The block on the other core is invalid
                        # RELEASE THE OTHER CORE CACHE
                        self.__core_instance.release_other_core_cache()
                else:
                    # Can't get the locks
                    return LOCK_ERROR
            # Check if the block is invalid or not in self cache, or if the RL isnt the needed value
            if (mem_address_on_cache and mem_address_state_on_cache == StatesEnum.INVALID) or \
                    (not mem_address_on_cache):

                # or (self.__core_instance.get_self_rl != mem_add_to_store):
                # Not on self cache or invalid on self cache, or the RL isnt the needed value

                total_execution_clock_cycles += self.solve_cache_miss(mem_add_to_store)
                if self.__core_instance.get_self_rl != mem_add_to_store:
                    # Set x2 to 0
                    self.__core_instance.set_register(source_registry, 0)
                    return total_execution_clock_cycles
        else:
            # Can't get self cache
            return LOCK_ERROR

        # The RL its correct
        # Store the register value on the cache block
        value_to_store = self.__core_instance.get_register_value(source_registry)
        self.__core_instance.change_word_value_data_cache(mem_add_to_store, value_to_store)
        # Returns the execution time
        return total_execution_clock_cycles

    # Method to solve cache miss, assumes that only self cache is locked
    def solve_cache_miss(self, m_address):
        clock_cycles = 0
        # LOCK OTHER CORE CACHE AND DATA BUS
        if self.__core_instance.acquire_other_and_data_bus_locks():
            # LOCKS ACQUIRED + 2 Other cache +32 Data bus
            clock_cycles += CONSULT_OTHER_CACHE_CLOCK_CYCLES + DATA_BUS_OPERATION_CLOCK_CYCLES
            if self.__core_instance.get_if_memory_address_on_other_cache(m_address) and \
                    self.__core_instance.get_memory_address_state_on_other_cache(m_address) == StatesEnum.MODIFIED:
                # Memory address is on the other core cache and other core cache block is modified
                # Store the other core block and get the new block
                data_block_to_insert = DataBlock(0)
                data_block_to_insert.copy_data_block(
                    self.__core_instance.store_other_core_data_cache_block_on_main_memory(
                        m_address, StatesEnum.INVALID))

                # Invalidate the RL on the other core, in the case that it was using a lr
                self.__core_instance.invalidate_other_core_rl(m_address)

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
            clock_cycles += self.__core_instance.store_block_on_self_cache(StatesEnum.SHARED, m_address,
                                                                           data_to_insert)
            return clock_cycles
        else:
            # Cant get the other core cache or data bus
            return LOCK_ERROR


