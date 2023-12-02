package main

import (
	"testing"
)

func TestExtractDigitsNormal(t *testing.T) {
	result := ExtractDigits("1abc3")
	expected := "13"

	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestExtractDigitsNone(t *testing.T) {
	result := ExtractDigits("abcde")
	expected := ""

	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestExtractDigitsMix(t *testing.T) {
	result := ExtractDigits("a1bc3de5")
	expected := "15"

	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestExtractTextDigitsFirst(t *testing.T) {
	result := ExtractTextDigits("two1nine")
	expected := "219"
	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestExtractTextDigitsSecond(t *testing.T) {
	result := ExtractTextDigits("eightwothree")
	expected := "8wo3"
	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestExtractTextDigitsThird(t *testing.T) {
	result := ExtractTextDigits("7pqrstsixteen")
	expected := "7pqrst6teen"
	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestReplaceLastEnd(t *testing.T) {
	result := ReplaceLast("21nine", "nine", "9")
	expected := "219"
	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestReplaceLastMid(t *testing.T) {
	result := ReplaceLast("8wothreethreefr", "three", "3")
	expected := "8wothree3fr"
	if result != expected {
		t.Errorf("Expected %s, but got %s instead", expected, result)
	}
}

func TestDigits(t *testing.T) {
	result := GetDigitsFromLine("abcone2threexyz")

	expected := 13
	if result != expected {
		t.Errorf("Expected %d, but got %d instead", expected, result)
	}
}
