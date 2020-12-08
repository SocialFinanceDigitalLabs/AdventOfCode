const Part1 = require('./day07a');
const Part2 = require('./day07b');
var requireText = require('require-text');

let bagRules = requireText('./day07.txt', require);

console.log("Bag colors which can eventually contain at least one shiny gold bag:");
console.log(Part1(bagRules, "shiny gold"));

console.log("How many bags do we need?");
let result = Part2(bagRules, "shiny gold");
console.log("The number of bags we need is: " + result);
