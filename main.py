from InstructionMemory import InstructionMemory


def main():
    instruct_memory = InstructionMemory()
    test = int(input())
    print(instruct_memory.get_instruction(test))


main()

