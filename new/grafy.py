import sys
def nacti_graf(soubor):
    uzly = set()
    hrany = []
    naslednici = {}
    predchudci = {}

    with open(soubor, 'r', encoding='utf-8') as f:
        for radek in f:
            radek = radek.strip()
            if not radek:
                continue

            radek = radek.rstrip(';')
            casti = radek.split()

            typ = casti[0]

            if typ == 'u':
                # Zpracování uzlu
                uzel = casti[1]
                uzly.add(uzel)
                naslednici.setdefault(uzel, [])
                predchudci.setdefault(uzel, [])

            elif typ == 'h':
                # Zpracování hrany
                smer = '>' if '>' in casti else '<' if '<' in casti else '-'
                odkud, kam = (casti[1], casti[3]) if smer in ('>', '-') else (casti[3], casti[1])

                ohodnoceni = next((int(c) for c in casti[4:] if c.lstrip('-').isdigit()), None)
                nazev = next((c[1:] for c in casti[4:] if c.startswith(':')), None)

                # Pokud není název hrany, vygenerujeme jej jako kombinaci uzlů
                if nazev is None:
                    nazev = f"{odkud}{kam}"

                hrana = (odkud, kam, ohodnoceni, nazev)
                hrany.append(hrana)
                naslednici.setdefault(odkud, []).append(kam)
                predchudci.setdefault(kam, []).append(odkud)
                if smer == '-':
                    hrana_reverzni = (kam, odkud, ohodnoceni, nazev)
                    hrany.append(hrana_reverzni)
                    naslednici.setdefault(kam, []).append(odkud)
                    predchudci.setdefault(odkud, []).append(kam)

    return sorted(uzly), hrany, naslednici, predchudci

def pocet_hran():
    return hrany.count

def pocet_uzlu():
    return uzly.count

def kontrola_ohodnoceni(hrany):
    for hrana in hrany:
        if hrana[2] is None:
            return False
    return True

def kontrola_orientovanosti(hrany):
    for hrana in hrany:
        if hrana in [(h[1], h[0], h[2], h[3]) for h in hrany if h[0] != h[1]]:
            return False
    return True

def kontrola_souvislosti(uzly, sousedni_hrany):
    from collections import deque

    if not uzly:
        return True

    navstivene = set()
    queue = deque([next(iter(uzly))])

    while queue:
        uzel = queue.popleft()
        if uzel not in navstivene:
            navstivene.add(uzel)
            queue.extend(sousedni_hrany.get(uzel, []))

    return navstivene == uzly

def kontrola_slabe_souvislosti(uzly, sousedni_hrany):
    from collections import deque

    if not uzly:
        return True

    # Převod grafu na neorientovaný
    neorientovane_hrany = {uzel: set() for uzel in uzly}
    for uzel, sousede in sousedni_hrany.items():
        for soused in sousede:
            neorientovane_hrany[uzel].add(soused)
            neorientovane_hrany[soused].add(uzel)

    navstivene = set()
    queue = deque([next(iter(uzly))])

    while queue:
        uzel = queue.popleft()
        if uzel not in navstivene:
            navstivene.add(uzel)
            queue.extend(neorientovane_hrany.get(uzel, []))

    return navstivene == uzly

def kontrola_silne_souvislosti(uzly, sousedni_hrany):
    def dfs(uzel, navstivene, sousedni_hrany):
        navstivene.add(uzel)
        for soused in sousedni_hrany.get(uzel, []):
            if soused not in navstivene:
                dfs(soused, navstivene, sousedni_hrany)

    # Kontrola dosažitelnosti každého uzlu z každého jiného uzlu
    for start_uzel in uzly:
        navstivene = set()
        dfs(start_uzel, navstivene, sousedni_hrany)
        if navstivene != uzly:
            return False

    # Vytvoření reverzovaného grafu a kontrola dosažitelnosti opačně
    obracene_hrany = {uzel: [] for uzel in uzly}
    for uzel, sousede in sousedni_hrany.items():
        for soused in sousede:
            obracene_hrany[soused].append(uzel)

    for start_uzel in uzly:
        navstivene = set()
        dfs(start_uzel, navstivene, obracene_hrany)
        if navstivene != uzly:
            return False

    return True

def kontrola_bipartitnosti(uzly, hrany):
    barvy = {}

    for uzel in uzly:
        if uzel not in barvy:
            stack = [uzel]
            barvy[uzel] = 0

            while stack:
                vrchol = stack.pop()

                for u, v, _, _ in hrany:
                    if u == vrchol:
                        soused = v
                    elif v == vrchol:
                        soused = u
                    else:
                        continue

                    if soused not in barvy:
                        stack.append(soused)
                        barvy[soused] = 1 - barvy[vrchol]
                    elif barvy[soused] == barvy[vrchol]:
                        return False

    return True

def kontrola_prostosti(hrany):
    videne_hrany = set()
    for hrana in hrany:
        # Kontrola násobných hran
        hrana_bez_ohodnoceni = (hrana[0], hrana[1])
        if hrana_bez_ohodnoceni in videne_hrany:
            return False
        videne_hrany.add(hrana_bez_ohodnoceni)
    return True

def kontrola_jednoduchosti(hrany):
    videne_hrany = set()
    for hrana in hrany:
        # Kontrola násobných hran
        hrana_bez_ohodnoceni = (hrana[0], hrana[1])
        if hrana_bez_ohodnoceni in videne_hrany:
            return False
        videne_hrany.add(hrana_bez_ohodnoceni)
        # Kontrola smyček
        if hrana[0] == hrana[1]:
            return False
    return True

def kontrola_regulernosti(sousedni_hrany):
    stupne = [len(sousedni_hrany[uzel]) for uzel in sousedni_hrany]
    return all(stupen == stupne[0] for stupen in stupne)

def kontrola_uplnosti(uzly, hrany):
    pocet_uzlu = len(uzly)
    pozadovany_pocet_hran = pocet_uzlu * (pocet_uzlu - 1) // 2
    skutecny_pocet_hran = len(set((min(hrana[0], hrana[1]), max(hrana[0], hrana[1])) for hrana in hrany))
    return skutecny_pocet_hran == pozadovany_pocet_hran

def vystupni_okoli_hrany(hrany, uzel):
    vystupni_hrany = {hrana[3] for hrana in hrany if hrana[0] == uzel}
    return vystupni_hrany

def vstupni_okoli_hrany(hrany, uzel):
    vstupni_hrany = {hrana[3] for hrana in hrany if hrana[1] == uzel}
    return vstupni_hrany

#TODO celkový stupeň uzlu - rozlišit orientovaný a neorientovaný

def vstupni_stupen(predchudci, uzel):
    return len(predchudci.get(uzel, []))

def vystupni_stupen(naslednici, uzel):
    return len(naslednici.get(uzel, []))

def celkovy_stupen(naslednici, predchudci, uzel, hrany):
    orientovany = kontrola_orientovanosti(hrany)
    if orientovany:
        return vystupni_stupen(naslednici, uzel) + vstupni_stupen(predchudci, uzel)
    else:
        return vystupni_stupen(naslednici, uzel)

####### START: MATICE INCIDENCEC

def matice_incidence(uzly, hrany):
    # Seřadíme uzly a hrany podle abecedy
    uzly = sorted(uzly)

    # Odstraníme duplicity u neorientovaných hran
    unikatni_hrany = []
    videne_hrany = set()
    for hrana in hrany:
        odkud, kam, _, nazev = hrana
        if (kam, odkud) not in videne_hrany and (odkud, kam) not in videne_hrany:
            unikatni_hrany.append(hrana)
            videne_hrany.add((odkud, kam))

    # Zjistíme délku nejdelšího názvu hrany pro formátování
    max_delka_hrany = max(len(hrana[3]) for hrana in unikatni_hrany)
    sirka_sloupce = max(max_delka_hrany, 3) + 2  # minimální šířka + odsazení

    # Vytvoříme prázdnou matici incidence pro každý uzel
    matice = {uzel: [0] * len(unikatni_hrany) for uzel in uzly}

    # Naplnění matice incidence
    for i, hrana in enumerate(unikatni_hrany):
        odkud, kam, _, _ = hrana
        if odkud == kam:
            matice[odkud][i] = 2  # Smyčka
        elif kontrola_orientovanosti(hrany):
            matice[odkud][i] = 1  # Výstupní uzel (orientovaný graf)
            matice[kam][i] = -1  # Vstupní uzel (orientovaný graf)
        else:
            matice[odkud][i] = 1  # Výstupní uzel (neorientovaný graf)
            matice[kam][i] = 1   # Vstupní uzel (neorientovaný graf)

    return matice, uzly

def vypis_matice_incidence(matice, uzly, hrany):
    # Zjistíme délku nejdelšího názvu hrany pro formátování
    max_delka_hrany = max(len(hrana[3]) for hrana in hrany)
    sirka_sloupce = max(max_delka_hrany, 3) + 2  # minimální šířka + odsazení

    # Výpis hlavičky matice
    hlavicka = "     " + "   ".join(f"{hrana[3]:^{sirka_sloupce}}" for hrana in hrany)
    oddeleni = "     " + "-" * (len(hlavicka) - 5)
    print(hlavicka)
    print(oddeleni)

    # Výpis řádků matice pro každý uzel
    for uzel in uzly:
        radek = f"{uzel} | " + "   ".join(f"{hodnota:^{sirka_sloupce}}" for hodnota in matice[uzel])
        print(radek)


def vypis_bunky_incidence(matice, uzly, radek_index, sloupec_index):
    if matice is None:
        print("Matice incidence nebyla správně inicializována.")
        return

    if radek_index < len(matice) and sloupec_index < len(matice[uzly[0]]):
        hodnota = matice[uzly[radek_index]][sloupec_index]
        print(f"Hodnota v buňce na pozici řádek {radek_index + 1}, sloupec {sloupec_index + 1} v matici incidence: {hodnota}")
    else:
        print("nNeplatný index pro matici incidence.")

def vypocet_bunky_incidence_konkretni(matice, uzly, hrany, uzel=None, hrana=None):
    if matice is None:
        print("\nMatice incidence nebyla správně inicializována.")
        return

    if uzel is None or hrana is None:
        uzel = input('Zadejte uzel: ')
        hrana = input('Zadejte hranu (např. h1, h2, ...): ')
    print(f'Kontrolní výpis: uzel = {uzel}, hrana = {hrana}')

    if uzel in uzly:
        radek_index = uzly.index(uzel)
        try:
            sloupec_index = [hrana_data[3] for hrana_data in hrany].index(hrana)
        except ValueError:
            print(f"Chyba: hrana '{hrana}' nebyla nalezena v seznamu hran.")
            return
        hodnota = matice[uzel][sloupec_index]
        print(f"\nHodnota v buňce pro uzel '{uzel}' a hranu '{hrana}' v matici incidence: {hodnota}")
    else:
        print("\nNeplatný uzel nebo hrana pro matici incidence.")


def vypocet_bunky_sousednosti_konkretni(matice, uzly, uzel1=None, uzel2=None):
    if matice is None:
        print("\nMatice sousednosti nebyla správně inicializována.")
        return

    if uzel1 is None or uzel2 is None:
        uzel1 = input('Zadejte první uzel: ')
        uzel2 = input('Zadejte druhý uzel: ')
    print(f'Kontrolní výpis: uzel1 = {uzel1}, uzel2 = {uzel2}')

    if uzel1 in uzly and uzel2 in uzly:
        radek_index = uzly.index(uzel1)
        sloupec_index = uzly.index(uzel2)
        hodnota = matice[uzly.index(uzel1)][sloupec_index]
        print(f"\nHodnota v buňce pro uzel '{uzel1}' a uzel '{uzel2}' v matici sousednosti: {hodnota}")
    else:
        print("\nNeplatný uzel nebo uzly pro matici sousednosti.")


def vypocet_poctu_hodnot_incidence(matice):
    # Počet nul, jedniček, dvojek a mínus jedniček v matici incidence
    pocet_nul = sum(hodnota == 0 for radky in matice.values() for hodnota in radky)
    pocet_jednicek = sum(hodnota == 1 for radky in matice.values() for hodnota in radky)
    pocet_dvojek = sum(hodnota == 2 for radky in matice.values() for hodnota in radky)
    pocet_minus_jednicek = sum(hodnota == -1 for radky in matice.values() for hodnota in radky)
    print(f"\nPočet nul v matici incidence: {pocet_nul}")
    print(f"Počet jedniček v matici incidence: {pocet_jednicek}")
    print(f"Počet mínus jedniček v matici incidence: {pocet_minus_jednicek}")
    print(f"Počet dvojek (smyček) v matici incidence: {pocet_dvojek}")

####### START: MATICE SOUSEDNOSTI

def matice_sousednosti(uzly, hrany):
    # Seřadíme uzly podle abecedy
    uzly = sorted(uzly)

    # Vytvoříme prázdnou matici sousednosti
    matice = [[0 for _ in range(len(uzly))] for _ in range(len(uzly))]

    # Naplnění matice sousednosti
    uzel_index = {uzel: index for index, uzel in enumerate(uzly)}
    for hrana in hrany:
        odkud, kam, _, _ = hrana
        matice[uzel_index[odkud]][uzel_index[kam]] = 1

    return matice, uzly

def vypis_matici_sousednosti(matice, uzly):
    # Výpis hlavičky
    hlavicka = "    " + " ".join(f"{uzel:^{3}}" for uzel in uzly)
    oddeleni = "    " + "-" * (len(hlavicka) - 4)
    print(hlavicka)
    print(oddeleni)

    # Výpis řádků matice
    for i, uzel in enumerate(uzly):
        radek = f"{uzel} | " + " ".join(f"{hodnota:^{3}}" for hodnota in matice[i])
        print(radek)

    # Výpis počtu jednotlivých hodnot v matici
    hodnoty = {}
    for radek in matice:
        for hodnota in radek:
            if hodnota in hodnoty:
                hodnoty[hodnota] += 1
            else:
                hodnoty[hodnota] = 1

def nasobeni_matic_sousednosti(matice1, matice2):
    n = len(matice1)
    vysledek = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            vysledek[i][j] = sum(matice1[i][k] * matice2[k][j] for k in range(n))
    return vysledek

def vypocet_poctu_hodnot_sousednosti(matice):
    hodnoty = {}
    for radek in matice:
        for hodnota in radek:
            if hodnota in hodnoty:
                hodnoty[hodnota] += 1
            else:
                hodnoty[hodnota] = 1

    print(f"Počty hodnot v matici sousednosti:")
    for hodnota, pocet in sorted(hodnoty.items()):
        print(f"Value {hodnota}: {pocet}")

def matice_na_mocninu(matice, mocnina):
    vysledek = matice
    for _ in range(1, mocnina):
        vysledek = nasobeni_matic_sousednosti(vysledek, matice)
    return vysledek

def vypis_bunky_sousednosti(matice, uzly, radek_index, sloupec_index):
    if matice is None:
        print("Matice sousednosti nebyla spravne inicializovana.")
        return

    if radek_index < len(matice) and sloupec_index < len(matice[0]):
        hodnota = matice[radek_index][sloupec_index]
        print(f"Hodnota v bunce na pozici radek {radek_index + 1}, sloupec {sloupec_index + 1} v matici sousednosti: {hodnota}")
    else:
        print("Neplatny index pro matici sousednosti.")

############## END: MATICE SOUSEDNOSTI

#TODO vypiš info x-tého uzlu
#TODO vypiš info x-té hrany

def vypis_info_uzlu(hrany, naslednici, predchudci):
    # Získání uzlu od uživatele
    uzel = input('Zadejte uzel pro zobrazení informací: ')

    print(f"\nInformace pro uzel {uzel}:")
    print(f"Výstupní okolí: {vystupni_okoli_hrany(hrany, uzel)}")
    print(f"Vstupní okolí: {vstupni_okoli_hrany(hrany, uzel)}")
    print(f"Výstupní stupeň: {vystupni_stupen(naslednici, uzel)}")
    print(f"Vstupní stupeň: {vstupni_stupen(predchudci, uzel)}")
    print(f"Celkový stupeň: {celkovy_stupen(naslednici, predchudci, uzel, hrany)}")
    print(f"Následníci: {naslednici.get(uzel, [])}")
    print(f"Předchůdci: {predchudci.get(uzel, [])}")

def vypis_info_hrany(hrany):
    # Získání názvu hrany od uživatele
    hrana_nazev = input("Zadejte název hrany pro zobrazení informací: ")

    for hrana in hrany:
        if hrana[3] == hrana_nazev:
            print(f"\nInformace pro hranu {hrana_nazev}:")
            print(f"Odkud: {hrana[0]}")
            print(f"Kam: {hrana[1]}")
            print(f"Ohodnocení: {hrana[2]}")
            return
    print(f"\nHrana {hrana_nazev} nebyla nalezena.")

def vypis_vlastnosti_grafu(hrany, uzly, naslednici, predchudci):
    je_ohodnoceny = kontrola_ohodnoceni(hrany)
    je_orientovany = kontrola_orientovanosti(hrany)
    je_uplny = False if je_orientovany else kontrola_uplnosti(uzly, hrany)  # Orientovaný graf nemůže být úplný
    je_slabe_souvisly = kontrola_slabe_souvislosti(uzly, naslednici)
    je_silne_souvisly = kontrola_silne_souvislosti(uzly, naslednici)
    je_regulerni = je_uplny or kontrola_regulernosti(naslednici)  # Pokud je graf úplný, je také regulární
    je_bipartitni = kontrola_bipartitnosti(uzly, hrany)
    je_prosty = kontrola_prostosti(hrany)
    je_jednoduchy = kontrola_jednoduchosti(hrany)
    print("\nVlastnosti grafu:")
    print("Graf je ohodnocený." if je_ohodnoceny else "Graf není ohodnocený.")
    print("Graf je orientovaný." if je_orientovany else "Graf není orientovaný.")
    print("Graf je slabě souvislý." if je_slabe_souvisly else "Graf není slabě souvislý.")
    print("Graf je silně souvislý." if je_silne_souvisly else "Graf není silně souvislý.")
    print("Graf je prostý." if je_prosty else "Graf není prostý.")
    print("Graf je jednoduchý." if je_jednoduchy else "Graf není jednoduchý.")
    print("Graf je úplný." if je_uplny else "Graf není úplný.")
    print("Graf je regulární." if je_regulerni else "Graf není regulární.")
    print("Graf je bipartitní." if je_bipartitni else "Graf není bipartitní.")

if __name__ == "__main__":
    soubor = '01.txt'

    print("hello")

    #Načtení grafu NIKDY NEKOMENTOVAT
    uzly, hrany, naslednici, predchudci = nacti_graf(soubor)


    # TODO Vlastnosti grafu
    vypis_vlastnosti_grafu(hrany, uzly, naslednici, predchudci)


    print("\nVypis info:")
    for i, hrana in enumerate(hrany, 1):
        print(f"{hrana[0]} -> {hrana[1]}, ohodnocení: {hrana[2]}, název: h{i}")

    # Uzly
   # print("\nUzly:")
   # print(", ".join(uzly))

    #print("\nHrany:")
    #hrany_vypis = ", ".join([f"h{i}" for i in range(1, len(hrany) + 1)])
    #print(hrany_vypis)

## TODO K NICEMU

    #pocet_uzlu = sum(matice.values() for hodnota in radky)

    """
    # Uzly
    print("\nUzly:")
    print(", ".join(uzly))

    # Vypis info
    print("\nVypis info:")
    for i, hrana in enumerate(hrany, 1):
        print(f"{hrana[0]} -> {hrana[1]}, ohodnocení: {hrana[2]}, název: h{i}")

    # Hrany
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
"""



    print("\nInfo o uzlu a hranách")
    # Výpis informací o konkrétním uzlu
    #vypis_info_uzlu(hrany, naslednici, predchudci) #, A
    # Výpis informací o konkrétní hraně
    #vypis_info_hrany(hrany) #, AB
    matice_inc, uzly_inc = matice_incidence(uzly, hrany) #DEFINICE
    vypocet_poctu_hodnot_incidence(matice_inc) # INCIDENCE


## TODO K NICEMU


############ START: VÝPISY MATIC
    # Výpis matice incidence
   

 #   print("\nMatice sousednosti:")
 #   matice, uzly = matice_sousednosti(uzly, hrany)
#    matice_na_prvou = matice_na_mocninu(matice, 1)
#    vypis_matici_sousednosti(matice_na_prvou, uzly)  #VYPIS
 #   matice_na_treti = matice_na_mocninu(matice, 3)
 #   vypocet_bunky_sousednosti_konkretni(matice_na_treti, uzly, hrany)
#    vypis_matici_sousednosti(matice_na_treti, uzly)  #VYPIS
    #todo SKRYTÝ VÝPIS
#    vypis_matice_incidence(matice_inc, uzly_inc, hrany) #VYPIS

"""
    matice, uzly = matice_sousednosti(uzly, hrany)
    matice_na_prvou = matice_na_mocninu(matice, 1)

    #todo SKRYTÝ VÝPIS
    matice_sous, uzly_sous = matice_sousednosti(uzly, hrany) #DEFINICE
    #vypis_matici_sousednosti(matice_sous, uzly_sous) #VYPIS

    matice_na_druhou = matice_na_mocninu(matice, 2)
#  vypis_matici_sousednosti(matice_na_druhou, uzly)  #VYPIS



#todo samotný výpis


"""

############ END: VÝPISY MATIC #############


########### POČTY HODNOT MATICE SOSUEDNOSTI A INCIDENCE
#    print("\nPocty hodnot matice incidence:")

"""
    print("\nPocty hodnot matice sousednosti:")
    print("\nPocty na prvou:")
#    vypocet_poctu_hodnot_sousednosti(matice_sous)
    print("\nPocty na druhou:")
#    vypocet_poctu_hodnot_sousednosti(matice_na_druhou)
    print("\nPocty na treti:")
#    vypocet_poctu_hodnot_sousednosti(matice_na_treti)

######## START: KONKRÉTNÍ BUŇKY
    print("\nKonkretní pozice výpis matice incidence:")
    # Výpis hodnoty buňky matice incidence, řádek 2, sloupec 1 (v parametru píš řádek-1 a sloupec-1)
#    vypis_bunky_incidence(matice_inc, uzly_inc, 1, 0)

    print("\nKonkretní pozice výpis buněk matice sousednosti:")
    # Výpis hodnoty buňky matice sousednosti, řádek 2, sloupec 1 (v parametru píš řádek-1 a sloupec-1)
#    vypis_bunky_sousednosti(matice_na_prvou, uzly, 1, 0)

####### KONKRETNI HRANY
   # vypocet_bunky_sousednosti_konkretni(matice_na_treti, uzly, hrany)
#    vypocet_bunky_incidence_konkretni(matice_inc, uzly_inc, hrany)


######## END: KONKRÉTNÍ BUŇKY

"""

def pocet_hodnot_na_diagonale(matice, hodnota):
    """
    Spočítá počet výskytů dané hodnoty na hlavní diagonále matice.
    
    Args:
        matice: Může být buď seznam seznamů (matice sousednosti) 
               nebo slovník (matice incidence)
        hodnota: Hodnota, kterou hledáme na diagonále
    
    Returns:
        int: Počet výskytů dané hodnoty na hlavní diagonále
    """
    pocet = 0
    
    # Pro matici sousednosti (seznam seznamů)
    if isinstance(matice, list):
        for i in range(len(matice)):
            if matice[i][i] == hodnota:
                pocet += 1
                
    # Pro matici incidence (slovník)
    elif isinstance(matice, dict):
        uzly = sorted(matice.keys())
        for i, uzel in enumerate(uzly):
            if i < len(matice[uzel]) and matice[uzel][i] == hodnota:
                pocet += 1
                
    return pocet