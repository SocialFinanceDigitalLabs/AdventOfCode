function parseLine(line) {
    const strings = line.split(" ");
    // Step 2: Filter out non-numeric words
    const numericWords = strings.filter(word => {
        // Check if the word is numeric and can be parsed as an integer
        const parsedInt = parseInt(word);
        return !isNaN(parsedInt) && parsedInt.toString() === word;
    });
    // Step 3: Convert numeric words to integers
    return numericWords.map(word => parseInt(word));
}

function readFile(filePath) {
    const fs = require("fs");
    try {
        // Read the file synchronously
        const data = fs.readFileSync(filePath, 'utf8');

        // Split the content into an array of lines
        const lines = data.split('\n');

        // Remove empty lines
        const nonEmptyLines = lines.filter(line => line.trim() !== '');

        return nonEmptyLines;
    } catch (error) {
        console.error(`Error reading file: ${error.message}`);
        return [];
    }
}

function Part1(filePath) {
    let total = 1;
    var data = readFile(filePath);
    const times = parseLine(data[0]);
    const distances = parseLine(data[1]);
    const races = times.map((time, index) => [time, distances[index]]);

    for (const [time, distance] of races) {
        const timings = Array.from({ length: Math.min(time, distance + 1) }, (_, i) => i);
        const successes = timings.filter(timing => (time - timing) * timing > distance);

        total *= successes.length;
    }

    return total;
}

function Part2(filePath) {
    var data = readFile(filePath);
    const time_strings = data[0].replace(/\s+/g, '').match(/\d+/g);
    const distance_strings = data[1].replace(/\s+/g, '').match(/\d+/g);

    const time = time_strings.map(value => parseInt(value)).join('');
    const distance = distance_strings.map(value => parseInt(value)).join('');

    // Takes about 2.096 seconds on puzzle input
    const successes = Array.from({ length: Math.min(time, distance + 1) }, (_, timing) => timing)
        .filter(timing => timing * (time - timing) > distance);
    return successes.length;
}


var filePath = "../../inputs/day06/input.txt"
var result = Part1(filePath);
console.log(result);
var result = Part2(filePath);
console.log(result);