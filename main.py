from CPU import CPU
from SimulationStatistics import SimulationStatistics

simulation_statistics = SimulationStatistics()


def main():

    # Ask the user for the hilillos to use
    hilillos_to_use = -1
    while hilillos_to_use != 0 and hilillos_to_use != 1 and hilillos_to_use != 2:
        result = input("Ingrese un 0 para correr el hilillo facilísimo, "
                                    "un 1 para los hilillos simples "
                                    "o un 2 para los hilillos de la prueba final(Para ayuda, digite una h)\n")
        if (str(result)).lower() == 'h':
            print("\n\nAYUDA: Para utilizar hilillos distintos de los que se encuentran en el directorio del proyecto, remplace"
                  " el hilillo que se encuentra en Hilillos/Hilillo-FACILISIMO, y luego seleccione 0 al correr el "
                  "programa\n\n")
        elif result.isdigit():
            hilillos_to_use = int(result)

        # Initialize CPU
    quantum = input("Ingrese el quantum\n")
    cpu = CPU(hilillos_to_use, int(quantum))

    # Start the simulation
    cpu.start_cores()


main()
