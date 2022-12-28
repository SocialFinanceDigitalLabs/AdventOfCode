from aoc_2022_kws.day_25 import base10_to_snafu, snafu_to_base10


def test_snafu_to_base10():
    assert snafu_to_base10("1") == 1
    assert snafu_to_base10("1=-0-2") == 1747
    assert snafu_to_base10("12111") == 906
    assert snafu_to_base10("2=0=") == 198


def test_base10_to_snafu():
    assert base10_to_snafu(0) == "0"
    assert base10_to_snafu(1) == "1"
    assert base10_to_snafu(2) == "2"
    assert base10_to_snafu(3) == "1="
    assert base10_to_snafu(4) == "1-"
    assert base10_to_snafu(5) == "10"
    assert base10_to_snafu(6) == "11"
    assert base10_to_snafu(7) == "12"
    assert base10_to_snafu(8) == "2="
    assert base10_to_snafu(9) == "2-"
    assert base10_to_snafu(10) == "20"
    assert base10_to_snafu(15) == "1=0"
    assert base10_to_snafu(20) == "1-0"
    assert base10_to_snafu(2022) == "1=11-2"
    assert base10_to_snafu(12345) == "1-0---0"
    assert base10_to_snafu(314159265) == "1121-1110-1=0"

    assert base10_to_snafu(4890) == "2=-1=0"
    assert base10_to_snafu(1747) == "1=-0-2"
    assert base10_to_snafu(314159265) == "1121-1110-1=0"
