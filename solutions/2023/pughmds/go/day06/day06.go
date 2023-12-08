package main

import (
    "fmt"
    "strconv"
    "strings"
    "bufio"
    "flag"
    "os"
)

func parseLine(line string) []int {
    fields := strings.Fields(line)
    result := make([]int, 0)

    for _, val := range fields {
        num, err := strconv.Atoi(val)
        if err == nil {
            result = append(result, num)
        }
    }

    return result
}

func run(data []string) int {
    times := parseLine(data[0])
    distances := parseLine(data[1])

    var total int

    for i := 0; i < len(times); i++ {
        time := times[i]
        distance := distances[i]

        var successes []int
        for timing := 0; timing < min(time, distance+1); timing++ {
            if (time-timing)*timing > distance {
                successes = append(successes, timing)
            }
        }

        if total == 0 {
            total = len(successes)
        } else {
            total *= len(successes)
        }
    }

    return total
}

func extractValue(input string) int {
    trimmedValue := strings.TrimSpace(strings.Split(input, ":")[1])
    value, err := strconv.Atoi(trimmedValue)
    if err != nil {
        fmt.Println("Error converting to int:", err)
        return 0
    }
    return value
}

func run_p2(data []string) int {
    timeString := strings.ReplaceAll(data[0], " ", "")
    distanceString := strings.ReplaceAll(data[1], " ", "")
    time := extractValue(timeString)
    distance := extractValue(distanceString)

    var successes []int
    for timing := 0; timing < min(time, distance+1); timing++ {
        if (time-timing)*timing > distance {
            successes = append(successes, timing)
        }
    }

    return len(successes)
}

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
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
        fmt.Println(run(lines))
    } else if part == 2 {
        fmt.Println(run_p2(lines))
    }
}
