"""
# PAIEŠKOS ALGORITMAI: BFS ir DFS
# Programa, kuri lygi du neinformuotus paieškos algoritmus (Plotinę ir Gylią paiešką)
# ir palygina jų efektyvumą skirtingose grafų struktūrose.
"""

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from typing import List, Tuple, Set, Optional
import random

# ============================================================================
# 1. PAIEŠKOS ALGORITMŲ IMPLEMENTACIJA
# ============================================================================

class PaieskaAlgoritmų:
    """
    Klasė, kurioje implementuoti BFS ir DFS paieškos algoritmai.
    Siekiama rasta kelią ir aplankytų mazgų skaičius.
    """
    
    def __init__(self, grafas):
        """
        Inicijuoja algoritmų klasę su grafu.
        
        Args:
            grafas: NetworkX grafo objektas
        """
        self.grafas = grafas
        self.aplankytų = set()
        self.kelias = []
        self.iš_kur = {}
    
    def bfs(self, pradžia, tikslas) -> Tuple[Optional[List], int, List]:
        """
        Breadth-First Search.
        Naudoja queue duomenų struktūrą.
        
        Args:
            pradžia: Pradžios mazgas
            tikslas: Tikslo mazgas
            
        Returns:
            - Rastas kelias (arba None)
            - Aplankytų mazgų skaičius
            - Visų aplankytų mazgų sąrašas
        """
        # Reinicijuojame duomenis
        self.aplankytų = set()
        self.iš_kur = {pradžia: None}
        eilė = deque([pradžia])
        aplankytų_sąrašas = []
        
        # BFS algoritmas
        while eilė:
            dabartinis = eilė.popleft()
            
            # Jei naudojame šį mazgą pirmą kartą
            if dabartinis not in self.aplankytų:
                self.aplankytų.add(dabartinis)
                aplankytų_sąrašas.append(dabartinis)
                
                # Jei radome tikslą
                if dabartinis == tikslas:
                    kelias = self._atkurti_kelią(tikslas)
                    return kelias, len(self.aplankytų), aplankytų_sąrašas
                
                # Pridedame visus mazgus į eilę
                for sąsedas in self.grafas.neighbors(dabartinis):
                    if sąsedas not in self.iš_kur:
                        self.iš_kur[sąsedas] = dabartinis
                        eilė.append(sąsedas)
        
        # Kelias nerastas
        return None, len(self.aplankytų), aplankytų_sąrašas
    
    def dfs(self, pradžia, tikslas) -> Tuple[Optional[List], int, List]:
        """
        Depth-First Search.
        Naudoja stack duomenų struktūrą arba rekursiją.
        
        Args:
            pradžia: Pradžios mazgas
            tikslas: Tikslo mazgas
            
        Returns:
            - Rastas kelias (arba None)
            - Aplankytų mazgų skaičius
            - Visų aplankytų mazgų sąrašas
        """
        # Reinicijuojame duomenis
        self.aplankytų = set()
        self.iš_kur = {pradžia: None}
        galinė = [pradžia]
        aplankytų_sąrašas = []
        
        # DFS algoritmas
        while galinė:
            dabartinis = galinė.pop()
            
            # Jei naudojame šį mazgą pirmą kartą
            if dabartinis not in self.aplankytų:
                self.aplankytų.add(dabartinis)
                aplankytų_sąrašas.append(dabartinis)
                
                # Jei radome tikslą
                if dabartinis == tikslas:
                    kelias = self._atkurti_kelią(tikslas)
                    return kelias, len(self.aplankytų), aplankytų_sąrašas
                
                # Pridedame visus mazgus į galinę
                # Pridedame atvirkščiai, kad gauti nuoseklius rezultatus
                for sąsedas in reversed(list(self.grafas.neighbors(dabartinis))):
                    if sąsedas not in self.iš_kur:
                        self.iš_kur[sąsedas] = dabartinis
                        galinė.append(sąsedas)
        
        # Kelias nerastas
        return None, len(self.aplankytų), aplankytų_sąrašas
    
    def _atkurti_kelią(self, tikslas) -> List:
        """
        Atkuria kelią nuo pradžios iki tikslo.
        
        Args:
            tikslas: Tikslo mazgas
            
        Returns:
            Kelias nuo pradžios iki tikslo
        """
        kelias = []
        dabartinis = tikslas
        
        while dabartinis is not None:
            kelias.append(dabartinis)
            dabartinis = self.iš_kur[dabartinis]
        
        kelias.reverse()
        return kelias


# ============================================================================
# 2. GRAFO GENERAVIMAS
# ============================================================================

def generuoti_atsitiktinį_grafą(n_mazgų: int, seed: int = None) -> nx.Graph:
    """
    Generuoja atsitiktinį nejungtą grafą naudojant Erdős–Rényi modelį.
    
    Args:
        n_mazgų: Mazgų skaičius
        seed: Atsitiktinumo sėkla
        
    Returns:
        NetworkX grafo objektas
    """
    if seed is not None:
        random.seed(seed)

    # Sukuriame grafą su tikimybe, kad kraštai bus tarp mazgų
    # Pradžioje naudojame didelę tikimybę, kad būtų tiltas tarp visų mazgų
    grafas = nx.erdos_renyi_graph(n_mazgų, p=0.15)
    
    # Jei grafas nėra jungtas, jį papildomai sujungiame
    while not nx.is_connected(grafas):
        # Randame neprijungtus komponentus
        komponentai = list(nx.connected_components(grafas))
        
        # Jungtiname juos tarpusavyje
        for i in range(len(komponentai) - 1):
            mazgas1 = list(komponentai[i])[0]
            mazgas2 = list(komponentai[i + 1])[0]
            grafas.add_edge(mazgas1, mazgas2)
    
    return grafas


# ============================================================================
# 3. TESTO VYKDYMAS
# ============================================================================

def vykdyti_testą(grafas, pradžia, tikslas, grafo_numeris: int):
    """
    Vykdo BFS ir DFS testą ant duoto grafo ir grąžina rezultatus.
    
    Args:
        grafas: NetworkX grafo objektas
        pradžia: Pradžios mazgas
        tikslas: Tikslo mazgas
        grafo_numeris: Grafo numeris spausdinimui
        
    Returns:
        Žodynas su rezultatais
    """
    print(f"\n{'-'*60}")
    print(f"GRAFAS #{grafo_numeris}")
    print(f"Mazgų skaičius: {grafas.number_of_nodes()}")
    print(f"Kraštų skaičius: {grafas.number_of_edges()}")
    print(f"Pradžia: {pradžia} -> Tikslas: {tikslas}")
    print(f"{'-'*60}\n")

    paieška = PaieskaAlgoritmų(grafas)

    # BFS vykdymas
    print("PLOTINĖ PAIEŠKA (BFS)")
    print("-" * 40)
    bfs_kelias, bfs_aplankyta, bfs_sąrašas = paieška.bfs(pradžia, tikslas)

    if bfs_kelias:
        print(f"Kelias rastas: {' -> '.join(map(str, bfs_kelias))}")
        print(f"  Kelio ilgis (kraštų): {len(bfs_kelias) - 1}")
    else:
        print(f"Kelias NERASTAS")
        print(f"  Kelio ilgis (kraštų): N/A")

    print(f"  Aplankyta mazgų: {bfs_aplankyta}")
    print()

    # DFS vykdymas
    print("GILI PAIEŠKA (DFS)")
    print("-" * 40)
    dfs_kelias, dfs_aplankyta, dfs_sąrašas = paieška.dfs(pradžia, tikslas)

    if dfs_kelias:
        print(f"Kelias rastas: {' -> '.join(map(str, dfs_kelias))}")
        print(f"  Kelio ilgis (kraštų): {len(dfs_kelias) - 1}")
    else:
        print(f"Kelias NERASTAS")
        print(f"  Kelio ilgis (kraštų): N/A")

    print(f"  Aplankyta mazgų: {dfs_aplankyta}")
    print()
    
    # Rezultatų grąžinimas
    return {
        'grafo_numeris': grafo_numeris,
        'mazgų_skaičius': grafas.number_of_nodes(),
        'kraštų_skaičius': grafas.number_of_edges(),
        'bfs_kelias': bfs_kelias,
        'bfs_kelio_ilgis': len(bfs_kelias) - 1 if bfs_kelias else None,
        'bfs_aplankyta': bfs_aplankyta,
        'dfs_kelias': dfs_kelias,
        'dfs_kelio_ilgis': len(dfs_kelias) - 1 if dfs_kelias else None,
        'dfs_aplankyta': dfs_aplankyta,
    }


# ============================================================================
# 4. PALYGINIMO LENTELĖS SPAUSDINIMAS
# ============================================================================

def spausdinti_palyginimo_lentelę(rezultatai: List[dict]):
    """
    Spausdina santrauke ir palygina visų testų rezultatus.
    
    Args:
        rezultatai: Rezultatų sąrašas iš vykdyti_testą
    """
    print("\n\n")
    print("-" * 80)
    print("PAIEŠKOS ALGORITMŲ PALYGINIMAS")
    print("-" * 80)
    print()
    
    print(f"{'Grafas':<10} {'Mazgai':<10} {'Kraštai':<10} {'Algoritm':<12} {'Kelias Rastas':<16} {'Kelio Ilgis':<15} {'Aplankyta':<12}")
    print("-" * 126)
    
    for rez in rezultatai:
        grafo_info = f"#{rez['grafo_numeris']}"
        mazgai = str(rez['mazgų_skaičius'])
        kraštai = str(rez['kraštų_skaičius'])
        
        # BFS eilutė
        bfs_rastas = "Taip" if rez['bfs_kelias'] else "Ne"
        bfs_ilgis = str(rez['bfs_kelio_ilgis']) if rez['bfs_kelio_ilgis'] is not None else "N/A"
        print(f"{grafo_info:<10} {mazgai:<10} {kraštai:<10} {'BFS':<12} {bfs_rastas:<16} {bfs_ilgis:<15} {str(rez['bfs_aplankyta']):<12}")
        
        # DFS eilutė
        dfs_rastas = "Taip" if rez['dfs_kelias'] else "Ne"
        dfs_ilgis = str(rez['dfs_kelio_ilgis']) if rez['dfs_kelio_ilgis'] is not None else "N/A"
        print(f"{' ':<10} {' ':<10} {' ':<10} {'DFS':<12} {dfs_rastas:<16} {dfs_ilgis:<15} {str(rez['dfs_aplankyta']):<12}")
        print("-" * 126)
    
    print()


# ============================================================================
# 5. ANALITINIS PALYGINIMAS
# ============================================================================

def spausdinti_analitinę_išvadą(rezultatai: List[dict]):
    """
    Spausdina analitinę išvadą apie algoritmų efektyvumą.
    
    Args:
        rezultatai: Rezultatų sąrašas iš vykdyti_testą
    """
    print("\n")
    print("-" * 80)
    print("ANALITINĖ IŠVADA")
    print("-" * 80)
    print()
    
    # Skaičiuojame vidutines reikšmes
    bfs_avg_aplankyta = sum(r['bfs_aplankyta'] for r in rezultatai) / len(rezultatai)
    dfs_avg_aplankyta = sum(r['dfs_aplankyta'] for r in rezultatai) / len(rezultatai)
    
    bfs_optimal_keliaiù = sum(1 for r in rezultatai if r['bfs_kelias'])
    dfs_optimal_keliaiù = sum(1 for r in rezultatai if r['dfs_kelias'])
    
    print(f"APLANKYTŲ MAZGŲ ANALIZĖ:")
    print(f"   - BFS vidutiniškai aplankė: {bfs_avg_aplankyta:.2f} mazgų")
    print(f"   - DFS vidutiniškai aplankė: {dfs_avg_aplankyta:.2f} mazgų")

    if bfs_avg_aplankyta < dfs_avg_aplankyta:
        skirtumas = ((dfs_avg_aplankyta - bfs_avg_aplankyta) / dfs_avg_aplankyta) * 100
        print(f"   -> BFS yra efektyvesnė: {skirtumas:.2f}% mažiau aplankytų mazgų")
    elif dfs_avg_aplankyta < bfs_avg_aplankyta:
        skirtumas = ((bfs_avg_aplankyta - dfs_avg_aplankyta) / bfs_avg_aplankyta) * 100
        print(f"   -> DFS yra efektyvesnė: {skirtumas:.2f}% mažiau aplankytų mazgų")
    else:
        print(f"   -> Abu algoritmai vienodai efektyvūs")

    print()
    print(f"KELIO RADIMO SĖKMĖ:")
    print(f"   - BFS rado kelius: {bfs_optimal_keliaiù}/{len(rezultatai)}")
    print(f"   - DFS rado kelius: {dfs_optimal_keliaiù}/{len(rezultatai)}")

    print()
    print(f"IŠVADOS:")
    print(f"   - BFS garantuoja trumpiausią kelią")
    print(f"   - DFS paprastai aplanko mažiau mazgų, bet kelias gali būti neoptimalus")
    print(f"   - BFS yra tikslesnė, kai reikalingas trumpiausias kelias")
    print(f"   - DFS yra efektyvesnė pagal atmintį (nenaudoja eilės)")
    
    print()
    print("-" * 80)


# ============================================================================
# 6. GRAFO VIZUALIZAVIMAS (PASIRINKTINIU)
# ============================================================================

def vizualizuoti_grafą(grafas, pradžia, tikslas, kelias, pavadinimas: str):
    """
    Vizualizuoja grafą su pažymėtu keliu.
    
    Args:
        grafas: NetworkX grafo objektas
        pradžia: Pradžios mazgas
        tikslas: Tikslo mazgas
        kelias: Rastas kelias
        pavadinimas: Pavadinimas
    """
    plt.figure(figsize=(12, 8))
    
    # Sukuriame išdėstymą
    pozicijos = nx.spring_layout(grafas, seed=42, iterations=50)
    
    # Piešiame visus kraštus
    nx.draw_networkx_edges(grafas, pozicijos, width=0.5, alpha=0.5)
    
    # Nustatome mazgų spalvas
    mazgų_spalvos = []
    for mazgas in grafas.nodes():
        if mazgas == pradžia:
            mazgų_spalvos.append('green')  # Žalia - pradžia
        elif mazgas == tikslas:
            mazgų_spalvos.append('red')    # Raudona - tikslas
        elif kelias and mazgas in kelias:
            mazgų_spalvos.append('yellow')  # Geltona - kelio dalis
        else:
            mazgų_spalvos.append('lightblue')  # Šviesiai mėlyna - kiti
    
    # Piešiame mazgus
    nx.draw_networkx_nodes(grafas, pozicijos, node_color=mazgų_spalvos, 
                           node_size=500, alpha=0.9)
    
    # Piešiame etiketės
    nx.draw_networkx_labels(grafas, pozicijos, font_size=8, font_weight='bold')
    
    plt.title(pavadinimas, fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Saugome paveikslą
    plt.savefig(f"{pavadinimas.replace(' ', '_')}.png", dpi=150, bbox_inches='tight')
    print(f"Grafas išsaugotas: {pavadinimas}.png")
    plt.close()


# ============================================================================
# 7. PAGRINDINĖ PROGRAMA
# ============================================================================

def main():
    """
    Pagrindinė programos funkcija.
    Generuoja 3 atsitiktinius grafus ir vykdo testus.
    """
    print("\n")
    print("-" * 80)
    print("PAIEŠKOS ALGORITMAI: PLOTINĖ (BFS) vs GILI (DFS) PAIEŠKA")
    print("Neinformuota Paieška Grafuose")
    print("-" * 80)
    
    # 3 atsitiktiniai grafai
    grafo_konfigūracijos = [
        {'n_mazgų': 25, 'seed': 42},
        {'n_mazgų': 30, 'seed': 123},
        {'n_mazgų': 35, 'seed': 456},
    ]
    
    rezultatai = []
    
    # Generuojame ir testuojame kiekvieną grafą
    for i, konfigūracija in enumerate(grafo_konfigūracijos, 1):
        # Generuojame grafą
        grafas = generuoti_atsitiktinį_grafą(**konfigūracija)
        
        # Pasirenkame atsitiktines pradžios ir tikslo mazgų
        mazgai_sąrašas = list(grafas.nodes())
        pradžia = mazgai_sąrašas[0]
        tikslas = mazgai_sąrašas[-1]
        
        # Vykdome testą
        rezultatas = vykdyti_testą(grafas, pradžia, tikslas, i)
        rezultatai.append(rezultatas)
        
        # Vizualizuojame grafą (pasirinktiniu)
        kelias_bfs = rezultatas['bfs_kelias']
        vizualizuoti_grafą(grafas, pradžia, tikslas, kelias_bfs, 
                          f"Grafas_{i}_BFS_Kelias")
    
    # Spausdiname rezultatus
    spausdinti_palyginimo_lentelę(rezultatai)
    spausdinti_analitinę_išvadą(rezultatai)

    print("\nPrograma baigė darbą.\n")


# ============================================================================
# 8. PROGRAMA STARTINA
# ============================================================================

if __name__ == "__main__":
    main()
