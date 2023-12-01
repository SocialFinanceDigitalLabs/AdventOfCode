package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func Part1() int {
	content, err := os.ReadFile("final.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(content), "\n")
	total := 0
	for _, line := range lines {
		var digits []int64
		for _, el := range line {
			s, err := strconv.ParseInt(string(el), 10, 8)
			if err == nil {
				digits = append(digits, s)
			}
		}

		if len(digits) == 0 {
			continue
		}
		value := strconv.FormatInt(digits[0], 10) + strconv.FormatInt(digits[len(digits)-1], 10)
		result, err := strconv.Atoi(value)
		if err == nil {
			total += result
		}
	}
	return total
}

func Part2() int {

	numbers := map[string]int64{
		"one":   1,
		"two":   2,
		"three": 3,
		"four":  4,
		"five":  5,
		"six":   6,
		"seven": 7,
		"eight": 8,
		"nine":  9,
	}
	content, err := os.ReadFile("final.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(content), "\n")
	total := 0
	for _, line := range lines {
		var digits []int64
		for i, el := range line {
			s, err := strconv.ParseInt(string(el), 10, 8)
			if err == nil {
				digits = append(digits, s)
			} else {
				for key, value := range numbers {
					last_index := i + len(key)
					if last_index > len(line) {
						continue
					}
					if line[i:last_index] == key {
						digits = append(digits, value)
					}
				}
			}
		}

		if len(digits) == 0 {
			continue
		}
		value := strconv.FormatInt(digits[0], 10) + strconv.FormatInt(digits[len(digits)-1], 10)
		result, err := strconv.Atoi(value)
		if err == nil {
			total += result
		}
	}
	return total
}

func main() {
	// total := Part1()
	total := Part2()

	fmt.Println(total)
}
