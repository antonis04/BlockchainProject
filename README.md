# BlockchainProject

Ten projekt demonstruje prosty system blockchain do przechowywania i weryfikacji dokumentów. Pozwala na dodawanie plików do blockchaina, wydobywanie bloków oraz sprawdzanie autentyczności dokumentów na podstawie ich obecności w łańcuchu bloków.

## Funkcjonalności
- Dodawanie dokumentów do kolejki oczekujących
- Wydobywanie bloków z dokumentami
- Weryfikacja, czy dokument znajduje się w blockchainie

## Szybki start

1. **Klonuj repozytorium lub pobierz pliki projektu.**
2. **Uruchom skrypt:**
   
   ```bash
   python main.py
   ```

3. **Przykładowe pliki** `umowa.txt` i `dyplom.pdf` zostaną utworzone automatycznie podczas uruchamiania.

## Przykład działania
Po uruchomieniu programu zobaczysz przykładowe wydobycie bloku oraz weryfikację dokumentów:

```
Weryfikacja dokumentów:
[✓] umowa.txt zweryfikowany! Data: ...
[✓] dyplom.pdf zweryfikowany! Data: ...
[✗] nieistniejacy.txt nie znaleziony w blockchainie!
```

## Wymagania
- Python 3.x

## Pliki
- `main.py` – główny plik z logiką blockchaina i testami
- `umowa.txt`, `dyplom.pdf` – przykładowe dokumenty

## Licencja
Projekt udostępniany na licencji MIT.

