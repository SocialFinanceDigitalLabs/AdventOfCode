from aoc_2022_kws.day_02 import Hands


def test_beats():
    assert Hands.ROCK.beats == Hands.SCISSORS


def test_looses_to():
    assert Hands.ROCK.looses_to == Hands.PAPER


def test_beats_hand():

    assert Hands.ROCK.beats_hand(Hands.SCISSORS)
    assert Hands.PAPER.beats_hand(Hands.ROCK)
    assert Hands.SCISSORS.beats_hand(Hands.PAPER)

    assert not Hands.ROCK.beats_hand(Hands.PAPER)
    assert not Hands.PAPER.beats_hand(Hands.SCISSORS)
    assert not Hands.SCISSORS.beats_hand(Hands.ROCK)
