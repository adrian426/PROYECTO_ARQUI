SHARED_BLOCK_STATE = "C"
MODIFIED_BLOCK_STATE = "M"
INVALID_BLOCK_STATE = "I"


# Class to execute the LW instruction
class LW:

    # Start the instruction execution
    # Receives the core instance, and the instruction to execute
    # Returns the execution cycles of the instruction, -1 if the execute cant get the locks
    def execute(self, core_instance, instruction):

        # Set the values for the execution
        destination_registry = instruction[1]
        direction_registry = instruction[2]
        direction_immediate = instruction[3]
        total_execution_clock_cycles = 0

        # Calculate the direction of the memory address on memory
        memory_address_to_get = \
            core_instance.get_register_value(direction_registry) + direction_immediate

        # Check if there is a cache miss
        mem_address_on_cache = core_instance.get_if_mem_address_is_on_self_cache(memory_address_to_get)
        mem_address_block_invalid = \
            core_instance.get_memory_address_state_on_cache(memory_address_to_get) == INVALID_BLOCK_STATE

        if (mem_address_on_cache and mem_address_block_invalid) or not mem_address_on_cache:
            total_execution_clock_cycles += self.solve_cache_miss(memory_address_to_get, core_instance)
            # ToDo set the clock cycles on the CPU to wait

        # Load the value in the register
        core_instance.set_register(destination_registry,
                                   core_instance.get_data_cache_value(memory_address_to_get))
        # Returns the execution time
        return total_execution_clock_cycles

    # Method to solve cache miss
    def solve_cache_miss(self, memory_address_to_get, core_instance):
        clock_cycles = 0
        if core_instance.get_if_memory_address_on_other_cache(memory_address_to_get):
            # Memory address is on the other core cache
            if core_instance.get_memory_address_state_on_other_cache(
                    memory_address_to_get) != MODIFIED_BLOCK_STATE:
                # Other core cache block isn't modified
                # Only need to load to self cache
                if core_instance.acquire_self_cache_and_data_bus_locks(core_instance):
                    # Self cache and data bus locked
                    pass
                    # ToDo charge the block to cache and check the victim block
                else:
                    pass
                    # ToDo notify the core to wait to the next cycle and not to load the next instruction
            else:
                pass
                # The block is modified on the other core
                # ToDo store the block on the other cache
                #  and
        else:
            # Memory address isn't in the other core
            pass
        return clock_cycles


