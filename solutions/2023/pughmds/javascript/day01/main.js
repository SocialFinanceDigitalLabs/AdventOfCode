function getDigits(inputString) {
    // Use a regular expression to match all single-digit numbers
    const digits = inputString.match(/\d/g);
    var result = 0;
    if (digits && digits.length > 0) {
        // Get the first and last single-digit numbers
        const firstDigit = digits[0];
        const lastDigit = digits[digits.length - 1];

        // Concatenate the results
        result = firstDigit + lastDigit;
    }
    return result;
}

function Part1(filePath) {
    const fs = require("fs");
    const readline = require("readline");
    var total = 0;

    // Setup the read Interface stream to read the file
    const readInterface = readline.createInterface({
        input: fs.createReadStream(filePath),
    });

    // When a line is encountered, here's what you do...
    readInterface.on("line", function(line) {
        var digits = getDigits(line);
        total += parseInt(digits);
    })

    // When we reach the end of the file, we want to output the result
    readInterface.on("close", function() {
        console.log("The total was: ", total)
    })
}

//Part1("../../inputs/day01/test1.txt");
//Part1("../../inputs/day01/test2.txt");
Part1("../../inputs/day01/input.txt");

