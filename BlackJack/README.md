# Blackjack

### Blackjack – gra karciana, w której gracz stara się pokonać krupiera, zdobywając sumę punktów jak najbliższą 21, nie przekraczając jej.

## Instrukcja:

1. Na początku gry dealer (krupier) i gracz otrzymują po dwie karty. Karty gracza są widoczne od razu, natomiast u krupiera widoczna jest tylko jedna karta.  
2. Gracz ma do wyboru dwie opcje: **HIT** (dobranie kolejnej karty) lub **STAND** (pozostanie przy obecnej liczbie kart). Celem gracza jest zdobycie jak największej liczby punktów, nie przekraczając 21.  
3. Po zakończeniu ruchu przez gracza odkrywana jest druga karta krupiera. Jeśli krupier ma mniej niż 17 punktów, dobiera kolejne karty, aż osiągnie co najmniej 17 punktów.  
4. Po zakończeniu doboru przez krupiera system liczy punkty i wyświetla jeden z czterech wyników.

## Wartości kart:

- **A** – 1 lub 11 punktów  
- **K, Q, J, 10** – 10 punktów  
- **9** – 9 punktów  
- **8** – 8 punktów  
- **7** – 7 punktów  
- **6** – 6 punktów  
- **5** – 5 punktów  
- **4** – 4 punkty  
- **3** – 3 punkty  
- **2** – 2 punkty  

## Wyniki gry:

1. **Player bust** – gracz przekroczył 21 punktów  
2. **Player win** – gracz zdobył więcej punktów od krupiera, nie przekraczając 21  
3. **Dealer win** – krupier zdobył więcej punktów od gracza, nie przekraczając 21  
4. **Tie game** – remis, gracz i krupier zdobyli taką samą liczbę punktów  

## Użyte zasoby:

- [https://www.1001fonts.com/stiff-brush-jk-font.html ](https://www.1001fonts.com/stiff-brush-jk-font.html ) -- czcionka - (free to use)
- [https://kenney.nl/assets/playing-cards-pack](https://kenney.nl/assets/playing-cards-pack) -- karty - (free to use)
- [https://www.pygame.org/docs/](https://www.pygame.org/docs/) -- dokumentacja do pygame
- [https://chatgpt.com/](https://chatgpt.com/) -- ChatGPT - (darmowa wersja)
- [https://www.w3schools.com/python/](https://www.w3schools.com/python/) -- dokumentacja do python

## Użyte biblioteki:

- copy
- random
- pytest
- pygame
- os

# ENG VERSION

# Blackjack

### Blackjack is a card game where the player attempts to beat the dealer by obtaining a hand total as close to 21 as possible, without exceeding it.

## Instructions:

1. At the start of the game, both the dealer and the player receive two cards. The player's cards are fully visible, while only one of the dealer's cards is revealed.
2. The player can choose between two options: **HIT** (take another card) or **STAND** (keep the current hand). The player's goal is to maximize their score without going over 21.
3. Once the player stands, the dealer's second card is revealed. If the dealer's total is under 17 points, they must draw additional cards until their score reaches at least 17.
4. After the dealer finishes drawing, the system calculates the scores and displays one of four outcomes.

## Card Values:

* **A (Ace)** – 1 or 11 points
* **K, Q, J, 10** – 10 points
* **9** – 9 points
* **8** – 8 points
* **7** – 7 points
* **6** – 6 points
* **5** – 5 points
* **4** – 4 points
* **3** – 3 points
* **2** – 2 points

## Game Outcomes:

1. **Player bust** – The player's total exceeded 21 points.
2. **Player win** – The player scored higher than the dealer without exceeding 21.
3. **Dealer win** – The dealer scored higher than the player without exceeding 21.
4. **Tie game (Push)** – A draw; both the player and the dealer achieved the exact same score.

## Resources Used:

* [Stiff Brush JK Font](https://www.1001fonts.com/stiff-brush-jk-font.html) – Typography (Free to use)
* [Kenney Playing Cards Pack](https://kenney.nl/assets/playing-cards-pack) – Card assets (Free to use)
* [Pygame Documentation](https://www.pygame.org/docs/) – Graphics and game loop reference
* [ChatGPT](https://chatgpt.com/) – AI assistance (Free version)
* [W3Schools Python Tutorial](https://www.w3schools.com/python/) – Python programming reference

## Libraries Used:

* `copy`
* `random`
* `pytest`
* `pygame`
* `os`