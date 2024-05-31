#!/usr/bin/env python3

import os
import csv
import random
import difflib

#---Nastavení---

# Umístění zdrojové tabulky
adresar_skriptu = os.path.dirname(os.path.abspath(__file__))
umisteni_tabulky = os.path.join(adresar_skriptu, 'slovnik.csv')

# Přiřazení sloupce z tabulky k její funkci
SLOUPEC_SLOVO, SLOUPEC_PREKLAD, SLOUPEC_UROVEN = 0,1,2

#---Aplikace---

def spustit_aplikaci():
    
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
    # Ulozit nove hodnoty urovni jednotlivých slov do CSV souboru
    with open(umisteni_tabulky, "w", newline="") as soubor:
        zapis = csv.writer(soubor)
        zapis.writerows(vystup)
    print("\nHra skončena. Průběh uložen.")


if __name__ == "__main__":
    spustit_aplikaci()
    input('Dokončeno, zadej cokoli') # Vyčkání stisku klávesy pro ukončení