# **Game of Life Web**

Game of Life Web to interaktywna aplikacja webowa oparta na **Flasku**, symulująca "Grę w życie" Johna Conwaya. Umożliwia użytkownikom logowanie, edycję planszy, zapis i wczytywanie symulacji oraz pełną kontrolę nad przebiegiem gry.

## **🚀 Funkcje**
- 🔹 **Symulacja "Gry w życie" Conwaya** – dynamiczna symulacja zmian na planszy.
- 🔹 **Logowanie i rejestracja użytkowników** – zabezpieczona baza danych użytkowników.
- 🔹 **Zapisywanie i wczytywanie symulacji** – użytkownicy mogą przechowywać swoje ulubione układy.
- 🔹 **Interaktywna edycja planszy** – kliknięcia zmieniają stan komórek.
- 🔹 **Automatyczna animacja** – możliwość startu i zatrzymania symulacji.
- 🔹 **Losowe generowanie układów** – szybki start dla nowych użytkowników.
- 🔹 **Ciemny motyw i nowoczesny wygląd** – estetyczne UI z animacjami.

## **📦 Instalacja**
### **1. Pobierz repozytorium**
```sh
git clone https://github.com/twoj-uzytkownik/game-of-life-web.git
cd game-of-life-web
```

### **2. Stwórz i aktywuj wirtualne środowisko**
```sh
python -m venv .venv
source .venv/bin/activate  # Na Windows: .venv\Scripts\activate
```

### **3. Zainstaluj zależności**
```sh
pip install -r requirements.txt
```

### **4. Utwórz bazę danych**
```sh
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### **5. Uruchom aplikację**
```sh
python app.py
```
Otwórz przeglądarkę i przejdź do `http://127.0.0.1:5000/` 🚀

## **🖥️ Użycie**
1. **Zarejestruj się i zaloguj**.
2. **Edytuj planszę** klikając na komórki.
3. **Uruchom symulację** (`Start/Stop`).
4. **Zapisz swoją symulację** i wróć do niej później.
5. **Eksperymentuj z losowymi układami!** 🎲

## **📂 Struktura projektu**
```
game_of_life/
│── static/          # Pliki statyczne (CSS, JS)
│   ├── styles.css   # Stylowanie strony
│   ├── script.js    # Logika frontendu
│── templates/       # Szablony HTML
│   ├── index.html   # Strona główna
│   ├── login.html   # Logowanie
│   ├── register.html # Rejestracja
│   ├── saved_simulations.html # Zapisane symulacje
│── app.py           # Backend Flask
│── game.py          # Logika gry w życie
│── models.py        # Modele bazy danych SQLAlchemy
│── config.py        # Konfiguracja aplikacji
│── database.db      # Plik bazy SQLite
│── README.md        # Dokumentacja
```

## **🛠️ Technologie**
- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Canvas API)
- **Baza danych:** SQLite

## **📝 TODO / Możliwe ulepszenia**
- 📌 Dodanie obsługi różnych rozmiarów planszy
- 📌 Możliwość eksportu/importu symulacji do pliku
- 📌 Lepsze animacje przejść między generacjami
- 📌 Ranking najpopularniejszych symulacji użytkowników

## **📜 Licencja**
Ten projekt jest udostępniony na licencji **MIT** – możesz go dowolnie modyfikować i rozwijać! 🎉

## **👨‍💻 Autor**
Projekt stworzony przez [Twoje Imię] ✨. Jeśli masz pytania, daj znać! 🚀

