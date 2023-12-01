package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

type NumberObject struct {
	Value      string
	FirstIndex int
	LastIndex  int
}

type KeyPair struct {
	Key   string
	Value int
}

// Extracts digits from a string
func ExtractDigits(input string) string {
	var firstDigit, lastDigit rune

	for _, char := range input {
		if unicode.IsDigit(char) {
			if firstDigit == 0 {
				firstDigit = char
			}
			lastDigit = char
		}
	}

	if firstDigit == 0 {
		return ""
	}

	result := string(firstDigit) + string(lastDigit)
	return result
}

// Replaces the last occurance of a substring in a string
func ReplaceLast(input, substring, replacement string) (output string) {
	i := strings.LastIndex(input, substring)
	if i == -1 {
		return input
	}

	if strings.HasSuffix(input, substring) {
		return input[:i] + replacement
	}

	return input[:i] + replacement + input[i+len(substring):]
}

// Alters strings to switch word-digits to numerical
func ExtractTextDigits(input string) string {
	var keys []string
	var lowestKey = KeyPair{Key: "", Value: 99}
	var highestKey = KeyPair{Key: "", Value: -1}
	var num NumberObject
	numbers := map[string]NumberObject{
		"one":   NumberObject{Value: "1", FirstIndex: 0, LastIndex: 0},
		"two":   NumberObject{Value: "2", FirstIndex: 0, LastIndex: 0},
		"three": NumberObject{Value: "3", FirstIndex: 0, LastIndex: 0},
		"four":  NumberObject{Value: "4", FirstIndex: 0, LastIndex: 0},
		"five":  NumberObject{Value: "5", FirstIndex: 0, LastIndex: 0},
		"six":   NumberObject{Value: "6", FirstIndex: 0, LastIndex: 0},
		"seven": NumberObject{Value: "7", FirstIndex: 0, LastIndex: 0},
		"eight": NumberObject{Value: "8", FirstIndex: 0, LastIndex: 0},
		"nine":  NumberObject{Value: "9", FirstIndex: 0, LastIndex: 0},
	}

	// Populate the slice with keys from the map
	for key := range numbers {
		keys = append(keys, key)
	}

	for _, key := range keys {
		// Replace the first occurrence
		num = numbers[key]
		num.FirstIndex = strings.Index(input, key)
		num.LastIndex = strings.LastIndex(input, key)
		numbers[key] = num

		if num.FirstIndex < lowestKey.Value && num.FirstIndex != -1 {
			lowestKey.Value = num.FirstIndex
			lowestKey.Key = key
		}
		if num.LastIndex > highestKey.Value {
			highestKey.Value = num.LastIndex
			highestKey.Key = key
		}
	}

	input = strings.Replace(input, lowestKey.Key, numbers[lowestKey.Key].Value, 1)
	input = ReplaceLast(input, highestKey.Key, numbers[highestKey.Key].Value)
	return input
}

//Given a line of text, extract the first and last digits on a line (either numerical or word)
func GetDigitsFromLine(line string) int {
	line = ExtractTextDigits(line)
	digits, err := strconv.Atoi(ExtractDigits(line))
	if err != nil {
		fmt.Println("Error:", err)
		return 0
	}
	return digits
}

func PartOne(lines []string) int {
	digit_sum := 0
	for _, line := range lines {
		digits, err := strconv.Atoi(ExtractDigits(line))
		if err != nil {
			fmt.Println("Error:", err)
			return 0
		}
		digit_sum += digits
	}

	return digit_sum
}

func PartTwo(lines []string) int {
	digit_sum := 0
	for _, line := range lines {
		digits := GetDigitsFromLine(line)
		digit_sum += digits
	}

	return digit_sum
}

func main() {
	var filename string
	var part int

	// Parse the file
	flag.StringVar(&filename, "file", "", "The input file")
	flag.IntVar(&part, "part", 0, "Which part to run")
	flag.Parse()

	if filename == "" {
		fmt.Println("Please provide a file name using the -file flag.")
		os.Exit(1)
	}

	// Which Part to run
	if part == 0 {
		fmt.Println("Please provide which part to run using the -part flag.")
		os.Exit(1)
	}

	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	if part == 1 {
		fmt.Println(PartOne(lines))
	} else if part == 2 {
		fmt.Println(PartTwo(lines))
	}
}
