const PART_ONE = {
    "red": 12,
    "green": 13,
    "blue": 14
};

function checkLine(line) {
    var game_ok = true

    game_parts = line.split(":");
    game_number = parseInt(game_parts[0].split(" ")[1]);
    phases = game_parts[1].split(";")

    for (var phase of phases) {
        groups = phase.trim().split(",");
        for (var group of groups) {
            colours = group.trim().split(" ");
            if (PART_ONE[colours[1]] < parseInt(colours[0])) {
                game_ok = false;
                break;
            }
        }
    }

    if (game_ok) {
        return {"game": game_number, "result": true}
    } else {
        return {"game": game_number, "result": false}
    }
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
        answer = checkLine(line);
        if (answer["result"]) {
            total += answer["game"];
        }
    })

    // When we reach the end of the file, we want to output the result
    readInterface.on("close", function() {
        console.log("The total was: ", total)
    })
}



//Part1("../../inputs/day02/test1.txt");
Part1("../../inputs/day02/input.txt");