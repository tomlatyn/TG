import sys
from contextlib import redirect_stdout

from grafy import *

# ssh -oHostKeyAlgorithms=+ssh-dss login@akela.mendelu.cz

class FileAndConsoleWriter:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.file = open(filename, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def close(self):
        self.file.close()

def main():
    soubor = 'smycka.txt'
    output_file = 'output.txt'
    
    writer = FileAndConsoleWriter(output_file)
    sys.stdout = writer

    try:
        #Načtení grafu
        uzly, hrany, naslednici, predchudci = nacti_graf(soubor)

        # Vlastnosti grafu
        vypis_vlastnosti_grafu(hrany, uzly, naslednici, predchudci)

        print("\nPočet hran:", len(uzly))

        print("\nPočet uzlu:", len(hrany))

        print("\nVypis info:")
        for i, hrana in enumerate(hrany, 1):
            print(f"{hrana[0]} -> {hrana[1]}, ohodnocení: {hrana[2]}, název: h{i}")

        # Uzly
        print("\nUzly:")
        print(", ".join(uzly))

        print("\nHrany:")
        hrany_vypis = ", ".join([f"h{i}" for i in range(1, len(hrany) + 1)])
        print(hrany_vypis)

        # Následnici
        print("\nNásledníci:")
        for uzel, sousede in naslednici.items():
            print(f"{uzel}: {', '.join(sousede)}")

        # Předchůdci
        print("\nPředchůdci:")
        for uzel, predch in predchudci.items():
            print(f"{uzel}: {', '.join(predch)}")

        # Výpis výstupního okolí uzlů
        print("\nVýstupní okolí uzlů:")
        for uzel in uzly:
            vystupni = vystupni_okoli_hrany(hrany, uzel)
            if vystupni:
                print(f"{uzel}: {vystupni}")

        # Výpis vstupního okolí uzlů
        print("\nVstupní okolí uzlů:")
        for uzel in uzly:
            vstupni = vstupni_okoli_hrany(hrany, uzel)
            if vstupni:
                print(f"{uzel}: {vstupni}")

        # Výpis vstupního stupně uzlů
        print("\nVstupní stupeň uzlů:")
        for uzel in uzly:
            stupen = vstupni_stupen(predchudci, uzel)
            print(f"{uzel}: [{stupen}]")

        # Výpis výstupního stupně uzlů
        print("\nVýstupní stupeň uzlů:")
        for uzel in uzly:
            stupen = vystupni_stupen(naslednici, uzel)
            print(f"{uzel}: [{stupen}]")

        # Matice incidence
        print("\nMatice incidence:")
        matice_inc, uzly_inc = matice_incidence(uzly, hrany)
        #vypis_matice_incidence(matice_inc, uzly_inc, hrany)
        vypocet_poctu_hodnot_incidence(matice_inc)

        # Matice sousednosti
        print("\nMatice sousednosti:")
        matice_sous, uzly_sous = matice_sousednosti(uzly, hrany)
        # vypis_matici_sousednosti(matice_sous, uzly_sous)

        # Matice sousednosti na mocninu
        mocnina = 4
        print("\nMatice sousednosti na mocninu {}:".format(mocnina))
        matice_na_n = matice_na_mocninu(matice_sous, mocnina)
        vypis_matici_sousednosti(matice_na_n, uzly_sous)

        # Matice sousednosti na druhou
        # print("\nMatice sousednosti na druhou:")
        matice_na_druhou = matice_na_mocninu(matice_sous, 2)
        # vypis_matici_sousednosti(matice_na_druhou, uzly_sous)

        # Matice sousednosti na třetí
        # print("\nMatice sousednosti na třetí:")
        matice_na_treti = matice_na_mocninu(matice_sous, 3)
        # vypis_matici_sousednosti(matice_na_treti, uzly_sous)

        # Počty hodnot v maticích
        print("\nPočty hodnot v maticích sousednosti:")
        # print("První mocnina:")
        # vypocet_poctu_hodnot_sousednosti(matice_sous)
        # print("\nDruhá mocnina:")
        # vypocet_poctu_hodnot_sousednosti(matice_na_druhou)
        # print("\nTřetí mocnina:")
        # vypocet_poctu_hodnot_sousednosti(matice_na_treti)
        print("\n{}. mocnina:".format(mocnina))
        vypocet_poctu_hodnot_sousednosti(matice_na_n)

        # Konkrétní buňky matic
        print("\nKonkrétní buňky matice incidence:")
        vypis_bunky_incidence(matice_inc, uzly_inc, 1, 0)
        
        print("\nKonkrétní buňky matice sousednosti:")
        vypis_bunky_sousednosti(matice_sous, uzly_sous, 1, 0)

        cislo = 1
        matice = matice_inc
        print("\nPošet čísla {} v zadané matici na hlavní diagonále:".format(cislo), pocet_hodnot_na_diagonale(matice_inc, cislo))

    finally:
        sys.stdout = sys.__stdout__
        writer.close()

if __name__ == "__main__":
    main()