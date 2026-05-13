import heapq
import random
import json

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

        heap = []
        for idx, party in enumerate(eligible_parties):
            heapq.heappush(heap, (-party.votes, random.random(), idx, party))

        for _ in range(self.total_seats):
            if not heap:
                break
                
            neg_quotient, _, idx, party = heapq.heappop(heap)
            party.seats += 1
            next_quotient = party.votes / (party.seats + 1)
            heapq.heappush(heap, (-next_quotient, random.random(), idx, party))

    def save_to_json(self, filename: str = "wyniki_wyborow.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.parties], f, indent=4, ensure_ascii=False)
        print(f"\n[INFO] Wyniki zapisano do pliku {filename}")


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

    except ValueError:
        print("\n[BŁĄD] Wprowadzono nieprawidłowe dane. Oczekiwano wartości liczbowej.")

if __name__ == "__main__":
    main()