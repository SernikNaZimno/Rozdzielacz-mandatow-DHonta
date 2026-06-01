import heapq
import random
import json
import matplotlib.pyplot as plt

class Party:
    def __init__(self, name: str, votes: int):
        self.name = name
        self.votes = votes
        self.seats = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "votes": self.votes,
            "seats": self.seats
        }

class Election:
    def __init__(self, total_seats: int, threshold_percent: float = 0.05):
        self.total_seats = total_seats
        self.threshold = threshold_percent
        self.parties = []
        self.total_votes = 0

    def add_party(self, name: str, votes: int):
        if votes < 0:
            raise ValueError("Liczba głosów nie może być ujemna.")
        self.parties.append(Party(name, votes))
        self.total_votes += votes

    def allocate_seats(self):
        if not self.parties or self.total_seats <= 0:
            return

        min_votes = self.total_votes * self.threshold
        eligible_parties = [p for p in self.parties if p.votes >= min_votes]

        if not eligible_parties:
            print("Żadna partia nie przekroczyła progu wyborczego.")
            return

        # Inicjalizacja heap'a z ilorazami głosów/1 dla każdej partii
        heap = []
        for idx, party in enumerate(eligible_parties):
            quotient = party.votes / 1
            heapq.heappush(heap, (-quotient, random.random(), idx, party, 1))

        # Przydzielanie mandatów według metody D'Hondta
        for _ in range(self.total_seats):
            if not heap:
                break
                
            neg_quotient, _, idx, party, divisor = heapq.heappop(heap)
            party.seats += 1
            # Dodaj następny iloraz dla tej partii (głosy / (liczba_otrzymanych_mandatów + 1))
            next_quotient = party.votes / (divisor + 1)
            heapq.heappush(heap, (-next_quotient, random.random(), idx, party, divisor + 1))

    def save_to_json(self, filename: str = "wyniki_wyborow.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.parties], f, indent=4, ensure_ascii=False)
        print(f"\n[INFO] Wyniki zapisano do pliku {filename}")

    def plot_results(self):
        """Generuje wykres słupkowy wyników wyborów"""
        party_names = [p.name for p in self.parties]
        seats = [p.seats for p in self.parties]
        
        # Filtrujemy partie które otrzymały mandaty do wykresu
        eligible = [(name, seat) for name, seat in zip(party_names, seats) if seat > 0]
        
        if not eligible:
            print("[INFO] Brak partii do wyświetlenia na wykresie.")
            return
        
        names, seat_counts = zip(*eligible)
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(names, seat_counts, color='steelblue', edgecolor='navy', linewidth=1.5)
        
        # Dodaj wartości na słupkach
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Partie polityczne', fontsize=12, fontweight='bold')
        plt.ylabel('Liczba mandatów', fontsize=12, fontweight='bold')
        plt.title('Rozkład mandatów w wyborach parlamentarnych - Metoda D\'Hondta', 
                 fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.show()

def main():
    print("=== System Przydziału Mandatów - Metoda D'Hondta ===")
    try:
        num_parties = int(input("Podaj liczbę partii biorących udział w wyborach: "))
        if num_parties <= 0:
            print("Liczba partii musi być większa od zera.")
            return

        election_data = []
        for i in range(num_parties):
            name = input(f"Podaj nazwę partii {i+1}: ")
            votes = int(input(f"Podaj liczbę głosów dla '{name}': "))
            election_data.append((name, votes))

        total_seats = int(input("Podaj liczbę mandatów do przydzielenia: "))
        
        election = Election(total_seats)
        for name, votes in election_data:
            election.add_party(name, votes)

        print("\nPrzetwarzanie wyników...")
        election.allocate_seats()

        print("\n=== WYNIKI WYBORÓW ===")
        for party in sorted(election.parties, key=lambda p: p.seats, reverse=True):
            print(f"{party.name}: Głosy = {party.votes}, Mandaty = {party.seats}")

        election.save_to_json()
        election.plot_results()

    except ValueError:
        print("\n[BŁĄD] Wprowadzono nieprawidłowe dane. Oczekiwano wartości liczbowej.")

if __name__ == "__main__":
    main()