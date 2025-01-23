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
- ```run``` - uruchamia wszystkie poprzednie

### Komendy i opcje
#### ```show``` pobiera dane z API i wyświetla je w terminalu.
#### Składnia
```
python app.py show [-d data_początkowa data_końcowa]
```
#### Przykład
```
python app.py show -d 2024-12-01 2024-12-31
```

#### ```save``` pobiera dane z API i zapisuje je do bazy danych.
#### Składnia
```
python app.py save [-d data_początkowa data_końcowa]
```
#### Przykład:
```
python app.py save 2024-12-01 2024-12-31
```

#### ```analyze``` analizuje dane z podanego zakresu dat na podstawie bazy danych.
#### Składnia
```
python app.py analyze [-d data_początkowa data_końcowa]
```
#### Przykład
```
python app.py analyze -d 2024-12-01 2024-12-31
```

#### ```report``` generuje raport na podstawie danych z podanego zakresu dat lub wszystkich danych historycznych. 
Raport może być wygenerowany w formatach csv i/lub json i zawiera analizę dla wszystkich bądź jednej konkretnej waluty.
#### Składnia
```
python app.py report [-d data_początkowa data_końcowa] [-f csv|json] [-c kod_waluty|-ac|-ah]
```
Opcje:
- -d, --dates: Określa zakres dat jeżeli nie wybrano pełnych danych historycznych.
- -f, --format: Określa format raportu (np. csv, json lub oba).
- -c, --currency: Kod waluty (np. USD).
- -ac, --all-currencies: Uwzględnia wszystkie dostępne waluty.
- -ah, --all-historical-data: Uwzględnia wszystkie dane z bazy danych (nie wymaga podawania dat).
#### Przykład
```
python app.py report -d 2024-12-01 2024-12-31 -f csv json -c USD
```
```
python app.py report -d 2024-12-01 2024-12-31 -f json -ac
```
```
python app.py report -f csv -ah
```

#### ```run``` uruchamia cały proces. 
Pobieranie danych, zapisywanie do bazy, analizę i generowanie raportu.
#### Składnia
```
python main.py report [-d data_początkowa data_końcowa] [-f csv|json] [-c kod_waluty|-ac|-ah]
```
Opcje:
- -d, --dates: Określa zakres dat.
- -f, --format: Określa format raportu (np. csv, json lub oba).
- -c, --currency: Kod waluty (np. USD).
- -ac, --all-currencies: Uwzględnia wszystkie dostępne waluty.
- -ah, --all-historical-data: Uwzględnia wszystkie dane z bazy danych.
#### Przykład
```
python app.py run -d 2024-12-01 2024-12-31 -f csv json -c USD
```
```
python app.py run -d 2024-12-01 2024-12-31 -f json -ac
```
```
python app.py run -d 2024-12-01 2024-12-31 -f csv -ah
```

### UI
Jeśli użytkownik nie poda żadnej komendy, uruchomi się interfejs użytkownika, który poprowadzi.
