# Paieškos algoritmai grafuose

Praktinis darbas, kurio metu lyginami du neinformuoti paieškos algoritmai: Plotinė paieška (Breadth-First Search - BFS) ir Gyli paieška (Depth-First Search - DFS).

## Apie projektą
Programa sugeneruoja 3 atsitiktinius grafus (25, 30 ir 35 mazgų) ir abiem paieškos algoritmais ieško kelio tarp to paties pradžios ir tikslo mazgo. Po to atspausdina palyginimo lentelę, kurioje matosi:
- Ar kelias buvo rastas.
- Koks kelio ilgis.
- Kiek mazgų buvo aplankyta vykdant paiešką.

Taip pat programa nubraižo ir išsaugo grafų paveikslėlius (.png formatu) su pažymėtu rastu keliu.

## Reikalavimai
Pasirūpinkite, kad turite įdiegtas reikalingas bibliotekas:

```bash
pip install networkx matplotlib
```

## Paleidimas
Programą paleisti galite įprastai per Python:

```bash
#
py 1Intelektika_1Intelektika.py
```

## Rezultatai
Išvados spausdinamos terminale po testų, palyginant kuris algoritmas veikė efektyviau ir užėmė mažiau resursų (aplankytų mazgų kiekis), bei įvertinant rasto kelio trumpumą.
