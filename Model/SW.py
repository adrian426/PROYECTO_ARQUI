from DataMemory.DataBlock import DataBlock
from StatesEnum import StatesEnum
# from Core import Core


DATA_BUS_OPERATION_CLOCK_CYCLES = 32
CONSULT_OTHER_CACHE_CLOCK_CYCLES = 2
LOCK_ERROR = -1


# Class to execute the SW instruction
class SW:

    # Start the instruction execution
    # Receives the core instance, and the instruction to execute
    # Returns the execution cycles of the instruction, -1 if the execute cant get the locks
    def execute(self, core_instance, instruction):

        # Set the values for the execution
        source_registry = instruction.get_instruction()[2]
        direction_registry = instruction.get_instruction()[1]
        direction_immediate = instruction.get_instruction()[3]
        total_execution_clock_cycles = 0

        # Calculate the direction of the memory address on memory
        mem_add_to_store = \
            core_instance.get_register_value(direction_registry) + direction_immediate

        # Check if there is a cache miss
        # LOCK SELF CACHE!!
        if core_instance.acquire_self_cache():
            # Get self cache
            mem_address_on_cache = core_instance.get_if_mem_address_is_on_self_cache(mem_add_to_store)
            mem_address_state_on_cache = core_instance.get_memory_address_state_on_cache(mem_add_to_store)
            # Check if the block is shared
            if mem_address_on_cache and mem_address_state_on_cache == StatesEnum.SHARED:
                # SHARED ON SELF CACHE, CHECK THE OTHER CORE
                # LOCK OTHER CORE CACHE AND DATA BUS
                if core_instance.acquire_other_core_cache() and core_instance.acquire_data_bus():
                    # Get if the block is on the other core and get the state
                    mem_address_on_other_core = core_instance.get_if_memory_address_on_other_cache(mem_add_to_store)
                    mem_address_state_on_other_cache = core_instance.get_memory_address_state_on_other_cache(
                        mem_add_to_store)
                    # ToDo clock cycles other core
                    # ToDo LR a fail
                    if mem_address_on_other_core and mem_address_state_on_other_cache == StatesEnum.SHARED:
                        # The block is shared on the other core
                        core_instance.change_block_state_on_other_core_cache(mem_add_to_store, StatesEnum.INVALID)
                    else:
                        # The block on the other core is invalid
                        # RELEASE THE OTHER CORE CACHE
                        core_instance.release_other_core_cache()
                else:
                    # Can't get the locks
                    return LOCK_ERROR
            # Check if the block is invalid or not in self cache
            if (mem_address_on_cache and mem_address_state_on_cache == StatesEnum.INVALID) or not mem_address_on_cache:
                # Not on self cache or invalid on self cache
                cache_miss_cycles_result = self.solve_cache_miss(mem_add_to_store, core_instance)
                if cache_miss_cycles_result == LOCK_ERROR:
                    return LOCK_ERROR
                else:
                    total_execution_clock_cycles += cache_miss_cycles_result
        else:
            # Can't get self cache
            return LOCK_ERROR

        # Store the value in the register
        value_to_store = core_instance.get_register_value(source_registry)
        core_instance.set_data_block_main_memory()
        # core_instance.set_register(destination_registry,
        #                            core_instance.get_data_cache_value(memory_address_to_get))
        # Returns the execution time
        return total_execution_clock_cycles
    #
    # # Method to solve cache miss
    # def solve_cache_miss(self, m_address, core_instance):
    #     clock_cycles = 0
    #     # LOCK OTHER CORE CACHE AND DATA BUS
    #     if core_instance.acquire_other_core_cache() and core_instance.acquire_data_bus():
    #         # LOCKS ACQUIRED + 2 Other cache +32 Data bus
    #         clock_cycles += CONSULT_OTHER_CACHE_CLOCK_CYCLES + DATA_BUS_OPERATION_CLOCK_CYCLES
    #         if core_instance.get_if_memory_address_on_other_cache(m_address):
    #             # Memory address is on the other core cache
    #             if core_instance.get_memory_address_state_on_other_cache(
    #                     m_address) == MODIFIED_BLOCK_STATE:
    #                 # Other core cache block is modified
    #                 # Store the other core block and get the new block
    #                 data_block_to_insert = DataBlock(0)
    #                 data_block_to_insert.copy_data_block(
    #                     core_instance.store_other_core_data_cache_block_on_main_memory(m_address, SHARED_BLOCK_STATE))
    #                 clock_cycles += core_instance.store_block_on_self_cache(
    #                     SHARED_BLOCK_STATE, m_address, data_block_to_insert)
    #                 return clock_cycles
    #         # Memory address isn't in the other core or isn't modified
    #         # LOCK RELEASED OTHER CORE CACHE
    #         core_instance.release_other_core_cache()
    #         # Only need to load to self cache + 32
    #         main_memory_data_block = core_instance.get_data_block(m_address)
    #         data_to_insert = DataBlock(0)
    #         data_to_insert.copy_data_block(main_memory_data_block)
    #         clock_cycles += core_instance.store_block_on_self_cache(SHARED_BLOCK_STATE, m_address, data_to_insert)
    #         return clock_cycles
    #     else:
    #         # Cant get the other core cache
    #         return LOCK_ERROR


