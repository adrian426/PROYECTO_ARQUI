SHARED_BLOCK_STATE = "C"
MODIFIED_BLOCK_STATE = "M"
INVALID_BLOCK_STATE = "I"


# Class to execute the LW instruction
class LW:

    # Start the instruction execution
    # Receives the core instance, and the instruction to execute
    def execute(self, core_instance, instruction):

        # Set the values for the execution
        destination_registry = instruction[1]
        direction_registry = instruction[2]
        direction_immediate = instruction[3]

        # Calculate the direction of the memory address on memory
        memory_address_to_get = \
            core_instance.get_register_value(direction_registry) + direction_immediate

        # Check if there is a cache miss
        if core_instance.get_if_mem_address_is_on_self_cache(memory_address_to_get):
            if core_instance.get_memory_address_state_on_cache(memory_address_to_get) != INVALID_BLOCK_STATE:
                # C o M
                # Cache hit Happy path
                core_instance.set_register(destination_registry,
                                           core_instance.get_data_cache_value(memory_address_to_get))
                # Execution end
                # ToDo set the clock cycles on the CPU to wait
            else:
                # I
                # Cache miss no victim block
                self.solve_cache_miss(memory_address_to_get, core_instance)
                # ToDo set the clock cycles on the CPU to wait
                pass
        else:
            # Cache miss, victim?
            self.solve_cache_miss(memory_address_to_get, core_instance)

    # Method to solve cache miss
    def solve_cache_miss(self, memory_address_to_get, core_instance):
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


