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
                # Cache hit Happy path
                core_instance.set_register(destination_registry,
                                           core_instance.get_data_cache_value(memory_address_to_get))
                # Execution end
                # ToDo set the clock cycles on the CPU to wait
            else:
                # Cache miss
                self.solve_cache_miss(memory_address_to_get, core_instance)
                # ToDo set the clock cycles on the CPU to wait
                pass
        else:
            # Cache miss
            self.solve_cache_miss(memory_address_to_get, core_instance)

    def solve_cache_miss(self, memory_address_to_get, core_instance):
        if core_instance.get_if_memory_address_on_other_cache(memory_address_to_get):
            if core_instance.get_memory_address_state_on_other_cache(
                    memory_address_to_get) != MODIFIED_BLOCK_STATE:
                # Only need to load to self cache
                if self.acquire_self_cache_and_data_bus_locks(core_instance):
                    # Self cache and data bus locked
                    pass
                    # ToDo charge the block to cache and check the victim block

    # Try to acquire the self cache and data bus lock
    def acquire_self_cache_and_data_bus_locks(self, core_instance):
        if core_instance.acquire_self_cache():
            if core_instance.acquire_data_bus():
                return True
            else:
                core_instance.release_self_cache()
                return False
        return False
