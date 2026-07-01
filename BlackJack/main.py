import copy
import random
import pygame
import os

pygame.init()
# zmienne ktore wykorzystuje
suits = ["clubs", "diamonds", "hearts", "spades"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
one_deck = []

# pętla która tworzy jedna talie kart kazdej wartosci i kazdego koloru, jako lista tupli
for suit in suits:
    for value in values:
        one_deck.append(((suit, value)))


decks = 4
WIDTH = 1200
HEIGHT = 800
#ustawienie ekranu
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# napis BlackJack w lewym gornym rogu
pygame.display.set_caption("BlackJack")

# sciezka do pliku
BASE_DIR = os.path.dirname(__file__)
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font("assets/fonts/stiff-brush-jk/stiffbrushjk.otf", 30)
smaller_font = pygame.font.Font("assets/fonts/stiff-brush-jk/stiffbrushjk.otf", 26)
active = False
CARD_WIDTH = 240
CARD_HEIGHT = 230
card_back = pygame.image.load(os.path.join(BASE_DIR, "assets/images/cards/large/card_back.png")).convert_alpha()
card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))
card_images = {}
animations =[]

# sciezka do assetow kart
cards_path = os.path.join(BASE_DIR, "assets/images/cards/large")

FACE_MAP = {
    "J": ["j", "jack"],
    "Q": ["q", "queen"],
    "K": ["k", "king"],
    "A": ["a", "ace"]
}

for filename in os.listdir(cards_path):
    if not filename.endswith(".png"):
        continue

    name = filename.lower()

    # kolor
    suit = next((s for s in suits if s in name), None)

    # wartosc
    value = None

    # liczby
    for v in ["10", "9", "8", "7", "6", "5", "4", "3", "2"]:
        if v in name or v.zfill(2) in name:
            value = v
            break

    # figury, jako A, K, Q, J
    if not value:
        for face, keys in FACE_MAP.items():
            if any(k in name for k in keys):
                value = face
                break

    if suit and value:
        path = os.path.join(cards_path, filename)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        card_images[(suit, value)] = image

# win, loss, draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
initial_deal_step = 0

# wszytskie talie do gry
game_deck = copy.deepcopy(decks * one_deck)
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ["", "Player Busted!", "Player Wins!", "Dealer Wins:(", "Tie Game'_'"]

# rozdaje karty graczowi i dealerowi
# def deal_cards(current_hand, current_deck):
#     card = random.randrange(len(current_deck))
#     current_hand.append(current_deck[card])
#     current_deck.pop(card)
#     return current_hand, current_deck

def deal_cards_with_animations(current_hand, current_deck, target_x, target_y, reveal=True):
    card_index = random.randrange(len(current_deck))
    card = current_deck.pop(card_index)

    # animacja karty zaczyna sie poza ekranem
    animations.append({
        "card": card,
        "x": WIDTH + 50,
        "y": HEIGHT // 2,
        "target_x": target_x,
        "target_y": target_y,
        "hand": current_hand,
        "reveal": reveal
    })

# funckja dla animacji kart
def update_animations():
    speed = 0.12
    finish = []

    for animation in animations:
        animation["x"] += (animation["target_x"] - animation["x"]) * speed
        animation["y"] += (animation["target_y"] - animation["y"]) * speed

        screen.blit(card_images[animation["card"]], (animation["x"], animation["y"]))

        if abs(animation["target_x"] - animation["x"]) < 2 and abs(animation["target_y"] - animation["y"]) < 2:
            finish.append(animation)

    for animation in animations:
        animation["x"] += (animation["target_x"] - animation["x"]) * speed
        animation["y"] += (animation["target_y"] - animation["y"]) * speed

        # sprawdzamy reveal karty
        if animation.get("reveal", True):
            screen.blit(card_images[animation["card"]], (animation["x"], animation["y"]))
        else:
            screen.blit(card_back, (animation["x"], animation["y"]))

        if abs(animation["target_x"] - animation["x"]) < 2 and abs(animation["target_y"] - animation["y"]) < 2:
            animation["hand"].append(animation["card"])
            animations.remove(animation)

# rysuje stol do gry, jako zielone tlo oraz zolty okrag
def draw_table():
    screen.fill((10, 80, 30))
    pygame.draw.ellipse(
        screen,
        (0, 100, 0),
        (-200, 100, WIDTH + 400, HEIGHT - 150)
    )
    pygame.draw.ellipse(
        screen,
        (255, 215, 0),
        (-200, 100, WIDTH + 400, HEIGHT - 150),
        5
    )

# funkcja z cienmi dla tekstu
def draw_text_with_shadow(surface, text, font, color, shadow_color, pos, shadow_offset=(2, 2)):
    if not isinstance(text, str):
        text = str(text)

    shadow_surf = font.render(text, True, shadow_color)
    surface.blit(shadow_surf, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))

    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

# rysuje tabele zwyciestw, porazek, remisow z dodawaniem cieni
def draw_ui():
    margin_top = 10
    records_text = f"Wins: {records[0]}  Losses: {records[1]}  Draws: {records[2]}"
    draw_text_with_shadow(
        screen,
        records_text,  # string
        smaller_font,
        color="white",
        shadow_color="black",
        pos=(WIDTH // 2 - smaller_font.size(records_text)[0] // 2, margin_top),
        shadow_offset=(2, 2)
    )

    # wynik gracza po prawej stronie kart
    if my_hand:
        last_card_x = 70 + 70 * (len(my_hand) - 1)
        draw_text_with_shadow(
            screen,
            f"Player Score: {player_score}",
            font,
            color="white",
            shadow_color="black",
            pos=(last_card_x + CARD_WIDTH + 10, 550),
            shadow_offset=(2, 2)
        )

    # wynik dealera po prawej stronie kart
    if reveal_dealer and dealer_hand:
        last_card_x = 70 + 70 * (len(dealer_hand) - 1)
        draw_text_with_shadow(
            screen,
            f"Dealer Score: {dealer_score}",
            font,
            color="white",
            shadow_color="black",
            pos=(last_card_x + CARD_WIDTH + 10, 75),
            shadow_offset=(2, 2)
        )

# wyswietla  karty na ekranie z uzyciem assetow
def draw_cards(player, dealer, reveal):
    for i, card in enumerate(player):

        if any(animation["card"] == card for animation in animations):
            continue

        x = 70 + (70 * i)
        y = 390 + (5 * i)
        screen.blit(card_images[card], (x, y))

    for i, card in enumerate(dealer):
        if any(animation["card"] == card for animation in animations):
            continue
        x = 70 + (70 * i)
        y = 75 + (5 * i)

        # jesli dealera nie odkryta to pokazuje tylko jedna karte, i tylna strone drugiej
        if i == 1 and not reveal:
            screen.blit(card_back, (x, y))
        # inne karty normalnie  pierwsza karta dealera widzoczna
        elif i == 0 and not reveal:
            screen.blit(card_images[card], (x, y))
        else:
            screen.blit(card_images[card], (x, y))

#funckja ktora ustawia karty gracza w odpowiedniej pozycji
def player_cards(index):
    return 70 + 70 * index, 390 + 5 * index

# funkcja ktora ustawia karty dealera w odpowiedniej pozycji
def dealer_cards(index):
    return 70 + 70 * index, 75 + 5 * index

# liczymy jak najlepszy wynik dla gracza i dealera
def calculate_score(hand):
    score = 0
    aces = 0

    for card in hand:
        value = card[1]

        if value in ["J", "Q", "K", "10"]:
            score += 10
        elif value == "A":
            score += 11
            aces += 1
        else:
            score += int(value)

    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score

# funkcja ktora rysuje przyciski NEW GAME, HIT, STAND, NEW GAME(po zakonczonej rundzie)
def draw_buttons():
    buttons = []
    mouse_pos = pygame.mouse.get_pos()

    if not active:
        # gra nieaktywna, przycisk NEW GAME na srodku
        btn_w, btn_h = 300, 100
        x = (WIDTH - btn_w) // 2
        y = (HEIGHT - btn_h) // 2
        color = "#42a5f5" if not pygame.Rect(x, y, btn_w, btn_h).collidepoint(mouse_pos) else "#1976d2"
        deal = pygame.draw.rect(screen, color, [x, y, btn_w, btn_h], 0, 10)
        pygame.draw.rect(screen, "white", [x, y, btn_w, btn_h], 5, 10)
        draw_text_with_shadow(
            screen,
            "NEW GAME",
            font,
            color="white",
            shadow_color="black",
            pos=(x + btn_w // 2 - font.size("NEW GAME")[0] // 2, y + btn_h // 2 - font.size("NEW GAME")[1] // 2),
            shadow_offset=(3, 3)
        )
        buttons.append(deal)

    elif outcome != 0:
        #napis wyniku nad przyciskiem oraz przycisk NEW GAME po zakonczonej rundzie
        result_text = results[outcome]
        text_width, text_height = font.size(result_text)
        result_x = WIDTH // 2 - text_width // 2
        result_y = HEIGHT // 2 - 80
        draw_text_with_shadow(
            screen,
            result_text,
            font,
            color="white",
            shadow_color="black",
            pos=(result_x, result_y),
            shadow_offset=(3, 3)
        )
        btn_w, btn_h = 300, 80
        x = WIDTH // 2 - btn_w // 2
        y = result_y + text_height + 20
        color = "#ab47bc" if not pygame.Rect(x, y, btn_w, btn_h).collidepoint(mouse_pos) else "#6a1b9a"
        deal = pygame.draw.rect(screen, color, [x, y, btn_w, btn_h], 0, 10)
        pygame.draw.rect(screen, "black", [x, y, btn_w, btn_h], 5, 10)
        draw_text_with_shadow(
            screen,
            "NEW GAME",
            font,
            color="white",
            shadow_color="black",
            pos=(x + btn_w // 2 - font.size("NEW GAME")[0] // 2,
                 y + btn_h // 2 - font.size("NEW GAME")[1] // 2),
            shadow_offset=(2, 2)
        )
        buttons.append(deal)

    else:
        # Gra aktywna HIT i STAND wyswietlaja sie na dole
        btn_w, btn_h = 200, 80
        spacing = 50
        total_w = btn_w*2 + spacing
        x_start = (WIDTH - total_w) // 2
        y = HEIGHT - 150

        # HIT
        hit_color = "#66bb6a" if not pygame.Rect(x_start,y,btn_w,btn_h).collidepoint(mouse_pos) else "#388e3c"
        hit = pygame.draw.rect(screen, hit_color, [x_start, y, btn_w, btn_h], 0, 10)
        draw_text_with_shadow(
            screen,
            "HIT ME",
            font,
            color="white",
            shadow_color="black",
            pos=(x_start + btn_w // 2 - font.size("HIT ME")[0] // 2, y + btn_h // 2 - font.size("HIT ME")[1] // 2),
            shadow_offset=(2, 2)
        )
        buttons.append(hit)

        # STAND
        stand_color = "#ffa726" if not pygame.Rect(x_start + btn_w + spacing,y,btn_w,btn_h).collidepoint(mouse_pos) else "#f57c00"
        stand = pygame.draw.rect(screen, stand_color, [x_start + btn_w + spacing, y, btn_w, btn_h], 0, 10)
        draw_text_with_shadow(
            screen,
            "STAND",
            font,
            color="white",
            shadow_color="black",
            pos=(x_start + btn_w + spacing + btn_w // 2 - font.size("STAND")[0] // 2,
                 y + btn_h // 2 - font.size("STAND")[1] // 2),
            shadow_offset=(2, 2)
        )
        buttons.append(stand)

    return buttons

# funkcja sprawdza czy gra jest zakonczona na obecnym ruchu
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # sprawdzamy rozne scenariusze zwyciestwa albo porazki
    # 1: player bust(gracz przekroczyl dopuszczalna ilosc punktow), 2: win, 3: loss, 4: tie
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or dealer_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

# glowna petla gry
run = True
while run:
    timer.tick(fps)
    draw_table()
    draw_ui()
    # sprawdzamy wylosowane karty
    if initial_deal and not animations:
        if initial_deal_step == 0:
            x, y = player_cards(len(my_hand))
            deal_cards_with_animations(my_hand, game_deck, x, y)
            initial_deal_step += 1

        elif initial_deal_step == 1:
            x, y = dealer_cards(len(dealer_hand))
            deal_cards_with_animations(dealer_hand, game_deck, x, y)
            initial_deal_step += 1

        elif initial_deal_step == 2:
            x, y = player_cards(len(my_hand))
            deal_cards_with_animations(my_hand, game_deck, x, y)
            initial_deal_step += 1

        elif initial_deal_step == 3:
            x, y = dealer_cards(len(dealer_hand))
            deal_cards_with_animations(dealer_hand, game_deck, x, y, reveal=False)
            initial_deal = False
            initial_deal_step = 0

    # kiedy gra jest aktywna wyswietla wynik oraz karty
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        update_animations()

        if reveal_dealer and not animations:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                # dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                x, y = dealer_cards(len(dealer_hand))
                deal_cards_with_animations(dealer_hand, game_deck, x, y)
    buttons = draw_buttons()


    # event dla wylaczenia gry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # przyciemnienie przy kliknięciu na przycisk
            for btn in buttons:
                if btn.collidepoint(event.pos):
                    pygame.draw.rect(screen, "grey", btn, 0, 10)
                    pygame.display.update()
                    pygame.time.delay(100)

        elif event.type == pygame.MOUSEBUTTONUP:
            # NEW GAME kiedy gra nieaktywna
            if not active and len(buttons) >= 1 and buttons[0].collidepoint(event.pos):
                active = True
                initial_deal = True
                initial_deal_step = 0
                game_deck = copy.deepcopy(decks * one_deck)
                my_hand = []
                dealer_hand = []
                outcome = 0
                hand_active = True
                reveal_dealer = False
                add_score = True

            # HEW HAND gdy runda zakonczona
            elif outcome != 0 and len(buttons) >= 1 and buttons[0].collidepoint(event.pos):
                initial_deal = True
                initial_deal_step = 0
                game_deck = copy.deepcopy(decks * one_deck)
                my_hand = []
                dealer_hand = []
                outcome = 0
                hand_active = True
                reveal_dealer = False
                add_score = True
                dealer_score = 0
                player_score = 0

            # HIT i STAND gra aktywna outcome = 0
            elif active and outcome == 0 and len(buttons) >= 2:
                # HIT
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active and not animations:
                    # my_hand, game_deck = deal_cards(my_hand, game_deck)
                    x, y = player_cards(len(my_hand))
                    deal_cards_with_animations(my_hand, game_deck, x, y)
                # STAND
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer and not animations:
                    reveal_dealer = True
                    hand_active = False

    # jesli gracz przekroczy limit to gra zakonczona
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()