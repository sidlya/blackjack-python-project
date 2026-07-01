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