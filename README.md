# Aplikacja do przetwarzania danych z NBP API

## Wymagania
- Python 3.10+

---

## Sposób użycia

### Wywołanie podstawowe
Aplikacja udostępnia interfejs wiersza poleceń (CLI). Użytkownik może uruchomić różne funkcje za pomocą poniższych komend:
- ```show```
- ```save```
- ```analyze```
- ```report```
- ```run```

### Komendy i opcje
#### ```show``` pobiera dane z API i wyświetla je w terminalu.
#### Składnia
```
python app.py show [data_początkowa] [data_końcowa]
```
#### Przykład
```
python app.py show 2024-12-01 2024-12-31
```

#### ```save``` pobiera dane z API i zapisuje je do bazy danych.
#### Składnia
```
python app.py save [data_początkowa] [data_końcowa]
```
#### Przykład:
```
python app.py save 2024-12-01 2024-12-31
```

#### ```analyze``` analizuje dane z podanego zakresu dat na podstawie bazy danych.
#### Składnia
```
python app.py analyze  [data_początkowa] [data_końcowa]
```
#### Przykład
```
python app.py analyze 2024-12-01 2024-12-31
```

#### ```report``` generuje raport na podstawie danych z podanego zakresu dat. 
Raport może być wygenerowany w formatach csv i/lub json i zawiera analizę dla wszystkich bądź jednej konkretnej waluty.
#### Składnia
```
python app.py report [data_początkowa] [data_końcowa] [-f csv|json] [-c kod_waluty|--all]
```
Opcje:
- -f, --format: Określa format raportu (np. csv, json lub oba).
- -c, --currency: Kod waluty (np. USD).
- --all: Uwzględnia wszystkie dostępne waluty.
#### Przykład
```
python app.py report 2024-12-01 2024-12-31 -f csv json -c USD
```
```
python app.py report 2024-12-01 2024-12-31 -f json --all
```

#### ```run``` uruchamia cały proces. 
Pobieranie danych, zapisywanie do bazy, analizę i generowanie raportu.
#### Składnia
```
python main.py report [data_początkowa] [data_końcowa] [-f csv|json] [-c kod_waluty|--all]
```
Opcje:
- -f, --format: Określa format raportu (np. csv, json lub oba).
- -c, --currency: Kod waluty (np. USD).
- --all: Uwzględnia wszystkie dostępne waluty.
#### Przykład
```
python app.py report 2024-12-01 2024-12-31 -f csv json -c USD
```
```
python app.py report 2024-12-01 2024-12-31 -f json --all
```

### UI
Jeśli użytkownik nie poda żadnej komendy, uruchomi się interfejs użytkownika, który poprowadzi.
