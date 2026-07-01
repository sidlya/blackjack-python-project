import pytest

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

def test_calculate_score():
    result = calculate_score([("J", "10"), ("Q", "9")])
    assert result == 19

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

def test_check_endgame():
    result = check_endgame(True, 17, 22, 1, 0, True)
    result2 = check_endgame(True, 17, 21, 2, 0, True)
    assert result == (1, 0, True)
    assert result2 == (2, 0, True)