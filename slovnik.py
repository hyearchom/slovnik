#!/usr/bin/env python3

import os
import csv
import random
import difflib
import argparse

#---Nastavení---

# Řádkové argumenty
parser = argparse.ArgumentParser(
                    prog='Slovník',
                    description='Testování slovní zásoby přezkoušením')
parser.add_argument(
                '-a', '--add',
                help="""Vložit nové slovo do slovníku ve formátu:
                        slovo,překlad""")

# Umístění zdrojové tabulky
adresar_skriptu = os.path.dirname(os.path.abspath(__file__))
umisteni_tabulky = os.path.join(adresar_skriptu, 'slovnik.csv')

# Přiřazení sloupce z tabulky k její funkci
SLOUPEC_SLOVO, SLOUPEC_PREKLAD, SLOUPEC_UROVEN = 0,1,2

#---Aplikace---

def overit_pridani():
    nove_spojeni = parser.parse_args().add
    if nove_spojeni:
        pridat_slovo(nove_spojeni)
        return True
    else:
        return False


def pridat_slovo(zadani):
    # odstranění nechtěných velkých písmen
    zadani = zadani.lower()
    """Formátování na zápis:
            - s počátečním indexem 1
            - '\n' skončením na novém řádku
    """
    zadani = f'{zadani},1\n'

    with open(umisteni_tabulky, "a", newline="") as soubor:
        soubor.write(zadani)


def spustit_prezkouseni():
    
    data = ziskani_dat_tabulky()
    
    try:
        while True:
            vyber_procviceni = nejmene_procvicovana_slova(data)
            vybrany_radek = zvolit_nahodne_slovo(vyber_procviceni)

            # Zvolení typu otázky, na kterou se bude hra ptát
            typ_otazky = random.randint(1, 2)

            if typ_otazky == 1:  # Zeptat se na slovo v Češtině
                testovani_hrace(
                    vybrany_radek,
                    SLOUPEC_SLOVO,
                    SLOUPEC_PREKLAD,
                    "Přelož slovo: ",
                    "Tvůj překlad: "
                    )

            elif typ_otazky == 2:  # Zeptat se na slovo v cizím jazyce
                testovani_hrace(
                    vybrany_radek,
                    SLOUPEC_PREKLAD,
                    SLOUPEC_SLOVO,
                    "Přelož slovo do Angličtiny: ",
                    "Slovo v originále: "
                    )

            print() # Vypsat prázdný řádek na konci

    except KeyboardInterrupt:
        ulozit_postup_hrace(data)

def ziskani_dat_tabulky():
    # Přečtení dat z tabulky
    obsah = []
    with open(umisteni_tabulky, "r") as soubor:
        cteni = csv.reader(soubor)
        for radek in cteni:
            obsah.append(radek)

    obsah.pop(0)  # Odstranění nepotřebné hlavičky z dat
    return obsah


def nejmene_procvicovana_slova(zdroj):
    # Najdi slova s nejnižsí úrovní v tabulce
    nejnizsi_uroven = min(radek[SLOUPEC_UROVEN] for radek in zdroj)
    return [radek for radek in zdroj if radek[SLOUPEC_UROVEN] == nejnizsi_uroven]


def zvolit_nahodne_slovo(zdroj):
    # Zvol náhodné slovo
    return random.choice(zdroj)


def testovani_hrace(zdroj, sloupec_vychozi, sloupec_odpoved, instrukce, komentar_zadani):

    print(instrukce + zdroj[sloupec_vychozi])
    
    zadano_hracem = input(komentar_zadani)
    
    vyhodnotit_odpoved(zdroj[sloupec_odpoved], zadano_hracem, zdroj)


def vyhodnotit_odpoved(spravna_odpoved, odpoved_hrace, zdroj):

    # Nastavení hodnotících odpovědí programu
    potvrzeni = 'Správně! Slovo je přesně: '
    odmitnuti = 'Nesprávně! Správně je slovo: '
    
    pomer_shody = difflib.SequenceMatcher(None, odpoved_hrace, spravna_odpoved).ratio()

    if pomer_shody >= 0.8:
        print(potvrzeni + spravna_odpoved)
        soucasna_uroven = int(zdroj[SLOUPEC_UROVEN])
        if soucasna_uroven < 5:
            zdroj[SLOUPEC_UROVEN] = str(soucasna_uroven + 1)
    else:
        print(odmitnuti + spravna_odpoved)


def ulozit_postup_hrace(vystup):
    # Uložit nove hodnoty urovni jednotlivých slov do CSV souboru
    with open(umisteni_tabulky, "r+", newline="") as soubor:
        # Předejde přepisu hlavičky
        hlavicka = soubor.readline()
        soubor.seek(0)
        soubor.write(hlavicka)
        
        # Zapíše nové hodnoty úrovní
        zapis = csv.writer(soubor)
        zapis.writerows(vystup)
    print("\nHra skončena. Průběh uložen.")


if __name__ == "__main__":
    if not overit_pridani():
        spustit_prezkouseni()
    input('Dokončeno, zadej cokoli') # Vyčkání stisku klávesy pro ukončení