SHARED_BLOCK_STATE = "C"
MODIFIED_BLOCK_STATE = "M"
INVALID_BLOCK_STATE = "I"


# Class to execute the LW instruction
class LW:

    # Receives the core instance, and the instruction to execute
    def __init__(self, core_instance, instruction):
        self.__core_instance = core_instance
        self.__destination_registry = instruction[1]
        self.__direction_registry = instruction[2]
        self.__direction_immediate = instruction[3]

    # Start the instruction execution
    def execute(self):
        # Calculate the direction of the memory address on memory
        memory_address_to_get = \
            self.__core_instance.get_register_value(self.__direction_registry) + self.__direction_immediate

        # Check if there is a cache miss
        if self.__core_instance.get_if_mem_address_is_on_self_cache(memory_address_to_get):
            if self.__core_instance.get_memory_address_state_on_cache(memory_address_to_get) != INVALID_BLOCK_STATE:
                # Caché hit Happy path
                self.__core_instance.set_register(self.__destination_registry, self.__core_instance.get_data_cache_value(memory_address_to_get))
                # Execution end
                # ToDo set the clock cycles on the CPU to wait
            else:
                # Cache miss
                self.solve_cache_miss(memory_address_to_get)
                # ToDo set the clock cycles on the CPU to wait
                pass
        else:
            # Caché miss
            self.solve_cache_miss(memory_address_to_get)


    def solve_cache_miss(self, memory_address_to_get):
        if self.__core_instance.get_if_memory_address_on_other_cache(memory_address_to_get):
            if self.__core_instance.get_memory_address_state_on_other_cache(
                    memory_address_to_get) != MODIFIED_BLOCK_STATE:
                # Only need to load to self cache
                if self.acquire_self_cache_and_data_bus_locks():
                    # Self cache and data bus locked
                    pass
                    # ToDo charge the block to cache and check the victim block


    # Try to adquire the self cache and data bus lock
    def acquire_self_cache_and_data_bus_locks(self):
        if self.__core_instance.acquire_self_cache():
            if self.__core_instance.acquire_data_bus():
                return True
            else:
                self.__core_instance.release_self_cache()
                return False
        return False