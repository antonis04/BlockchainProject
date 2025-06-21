import hashlib
import json
import time
from typing import List, Dict, Optional


class Block:
    """
    Klasa reprezentująca pojedynczy blok w łańcuchu bloków.
    Przechowuje dane, hash poprzedniego bloku, nonce oraz własny hash.
    """
    def __init__(self, index: int, data: dict, previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Oblicza hash bloku na podstawie jego zawartości.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        """
        Wydobywa blok, szukając odpowiedniego nonce, aby hash zaczynał się od określonej liczby zer.
        """
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    """
    Klasa zarządzająca całym łańcuchem bloków oraz operacjami na dokumentach.
    """
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4
        self.create_genesis_block()
        self.pending_documents: Dict[str, str] = {}

    def create_genesis_block(self):
        """
        Tworzy blok genesis (początkowy blok w łańcuchu).
        """
        genesis_block = Block(0, {"documents": {}}, "0")
        self.chain.append(genesis_block)

    def get_last_block(self) -> Block:
        """
        Zwraca ostatni blok w łańcuchu.
        """
        return self.chain[-1]

    def add_document(self, file_path: str):
        """
        Dodaje dokument do kolejki oczekujących na zatwierdzenie (wydobycie).
        Oblicza hash pliku i zapisuje go tymczasowo.
        """
        # Oblicz hash dokumentu
        with open(file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Dodaj do kolejki oczekujących
        self.pending_documents[file_path] = file_hash
        print(f"Dokument dodany do kolejki: {file_path}")

    def mine_pending_documents(self):
        """
        Tworzy nowy blok z oczekującymi dokumentami i wydobywa go.
        Po wydobyciu blok jest dodawany do łańcucha, a kolejka oczekujących jest czyszczona.
        """
        if not self.pending_documents:
            print("Brak dokumentów do zatwierdzenia!")
            return

        # Przygotuj dane dla nowego bloku
        last_block = self.get_last_block()
        new_data = {"documents": self.pending_documents.copy()}

        # Stwórz i wydobój nowy blok
        new_block = Block(
            index=len(self.chain),
            data=new_data,
            previous_hash=last_block.hash
        )
        new_block.mine_block(self.difficulty)

        # Dodaj do łańcucha
        self.chain.append(new_block)
        self.pending_documents = {}
        print(f"Nowy blok wydobyty! Hash: {new_block.hash}")

    def verify_document(self, file_path: str) -> Optional[float]:
        """
        Weryfikuje, czy dokument znajduje się w blockchainie.
        Zwraca timestamp bloku, jeśli dokument został znaleziony, w przeciwnym razie None.
        """
        # Oblicz hash dokumentu
        with open(file_path, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()

        # Przeszukaj blockchain
        for block in self.chain[1:]:  # Pomijamy blok genesis
            for path, doc_hash in block.data["documents"].items():
                if doc_hash == current_hash and path == file_path:
                    return block.timestamp

        return None

    def display_chain(self):
        """
        Wyświetla wszystkie bloki w łańcuchu wraz z ich zawartością.
        """
        print("\n" + "=" * 50 + " BLOCKCHAIN " + "=" * 50)
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {time.ctime(block.timestamp)}")
            print(f"Hash: {block.hash}")
            print(f"Poprzedni hash: {block.previous_hash}")
            print("Dokumenty:")
            for path, doc_hash in block.data["documents"].items():
                print(f"  - {path}: {doc_hash[:16]}...")
            print(f"Nonce: {block.nonce}")
            print("-" * 100)


# Testowanie systemu
if __name__ == "__main__":
    # Utwórz blockchain
    bc = Blockchain()

    # Utwórz przykładowe pliki
    with open("umowa.txt", "w") as f:
        f.write("To jest ważna umowa między stronami.")

    with open("dyplom.pdf", "wb") as f:
        f.write(b"PDF dokument z dyplomem uczelni")

    # Dodaj dokumenty do kolejki
    bc.add_document("umowa.txt")
    bc.add_document("dyplom.pdf")

    # Wydobój blok z dokumentami
    bc.mine_pending_documents()

    # Sprawdź weryfikację
    print("\nWeryfikacja dokumentów:")
    for doc in ["umowa.txt", "dyplom.pdf", "nieistniejacy.txt"]:
        timestamp = bc.verify_document(doc)
        if timestamp:
            print(f"[✓] {doc} zweryfikowany! Data: {time.ctime(timestamp)}")
        else:
            print(f"[✗] {doc} nie znaleziony w blockchainie!")

    # Dodaj dokumenty do kolejki
    bc.add_document("umowa.txt")
    bc.mine_pending_documents()

    # Walidacja istniejącego dokumentu
    wynik = bc.verify_document("umowa.txt")
    if wynik:
        print(f"Plik 'umowa.txt' jest w blockchainie, timestamp: {time.ctime(wynik)}")
    else:
        print("Plik 'umowa.txt' NIE został znaleziony w blockchainie!")

    # Próba walidacji nieistniejącego dokumentu
    nieistniejacy_plik = "nieistnieje.txt"
    try:
        wynik2 = bc.verify_document(nieistniejacy_plik)
        if wynik2:
            print(f"Plik '{nieistniejacy_plik}' jest w blockchainie, timestamp: {time.ctime(wynik2)}")
        else:
            print(f"UWAGA! Plik '{nieistniejacy_plik}' nie został znaleziony w blockchainie! Możliwe włamanie lub manipulacja!")
    except FileNotFoundError:
        print(f"Błąd: Plik '{nieistniejacy_plik}' nie znaleziony w Blockchainie!")

    # Wyświetl cały blockchain
    bc.display_chain()
