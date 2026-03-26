# 🇵🇱 polska-flaga

Nostalgiczna animacja flagi Polski na pełny ekran — hołd dla klasycznych dem z lat 90., które krążyły po polskim internecie jako małe pliki `.exe`.

Flaga odbija się od krawędzi ekranu (DVD-logo style), prędkość regulowana klawiaturą.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![pygame](https://img.shields.io/badge/pygame-2.1%2B-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Zrzut ekranu

```
┌─────────────────────────────────────────────────────┐
│  prędkość: 4.0x                          [ciemne tło]│
│                                                      │
│              ┌──────────────────────┐               │
│              │██████ BIAŁY ████████│               │
│              │█████ CZERWONY ██████│               │
│              └──────────────────────┘               │
└─────────────────────────────────────────────────────┘
```

---

## Wymagania

- Python 3.8+
- pygame 2.1+

```bash
pip install pygame
# lub
pip install -r requirements.txt
```

---

## Uruchomienie

```bash
python polska_flaga.py
```

Program uruchamia się od razu w trybie pełnoekranowym.

---

## Sterowanie

| Klawisz | Akcja |
|---------|-------|
| `+` / `=` | Przyspiesz |
| `-` | Zwolnij |
| `F` / `F11` | Przełącz pełny ekran / okno |
| `ESC` / `Q` | Wyjście |

Zakres prędkości: `0.5x` – `30.0x`

---

## Budowanie pliku .exe (Windows)

Jeśli chcesz standalone bez Pythona:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole polska_flaga.py
```

Plik wynikowy: `dist/polska_flaga.exe`

---

## Szczegóły techniczne

- Rozmiar flagi: `640×400` px (proporcja 5:8 zgodna z [Dz.U. 1980 nr 7 poz. 18](https://isap.sejm.gov.pl/))
- Barwy: biały `#FFFFFF`, karmazynowy `#DC143C`
- Ruch: wektor ukośny z odbiciami od krawędzi ekranu (klasyczny *bouncer*)
- Silnik: pygame, 60 FPS

---

## Licencja

MIT — rób co chcesz.

---

*Quaerendir*
