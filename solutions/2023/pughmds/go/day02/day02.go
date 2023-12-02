package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)


func PartOne(lines []string) int {
    var PART_ONE = map[string]int{
        "red":   12,
        "green": 13,
        "blue":  14,
    }
    total := 0

    for _, line := range lines {
        game_ok := true

        game_parts := strings.Split(line, ":")
        game_number, _ := strconv.Atoi(strings.Fields(game_parts[0])[1])
        phases := strings.Split(game_parts[1], ";")
        for _, phase := range phases {
            groups := strings.Split(strings.TrimSpace(phase), ",")
            for _, group := range groups {
                colours := strings.Split(strings.TrimSpace(group), " ")
                partOneValue, _ := strconv.Atoi(colours[0])
                if PART_ONE[colours[1]] < partOneValue {
                    game_ok = false
                    break
                }
            }
        }
        if game_ok {
            total += game_number
        }
    }
    return total
}

func PartTwo(lines []string) int {
    return 0
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
