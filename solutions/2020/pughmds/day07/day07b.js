const Part2 = (rulesText, bagToLookFor) => {
	// Initialise the bags dictionary
	let allBags = {};

	// Split the rules text into lines, and remove ending full stop
	let rules = rulesText.replace('.').split('\n');

	// Loop over the rules, one by one. We need to get the strings into a usable format
	for (let i = 0; i < rules.length; i++) {
		const rule = rules[i];

		// Get the first two words which would indicate the outer bag's colour
		const mainBagPattern = /^(\w*\s\w*)/gm;
		const [, mainBag] = mainBagPattern.exec(rule);
 
		// Make sure this outer bag is defined in our main object
		allBags[mainBag] = {
			innerTypes: {}
		};

		// Now, we need to parse the rest of the string and get each bag in the contents
		const contentsPattern = /(\d)+\s(\w*\s\w*)/gm;
		const contents = [ ...rule.matchAll(contentsPattern)];

		// Some bags will have nothing inside
		if (contents) {
			// Most bags will have several things inside
			contents.forEach(bag => {
				// Getting at the number of bags and the bag type in the contents
				const [, amount, bagType] = bag;

				// Set the bag's contents
				allBags[mainBag].innerTypes[bagType] = parseInt(amount.trim());
			});
		}
	}

	// Now that we have our structure, we can use recursion to sift through.
	// Start with a set to store the patterns we find
	function countBags(bagParent, child) {
		const children = allBags[child].innerTypes;
		const childKeys = Object.keys(children);
		let thisBags = 1;

		if (children.length === 0) {
			console.log("Found empty bag");
			return 1;
		}
	
		// Use recursion to look in the bags we've found in the contents
		for (let i = 0; i < childKeys.length; i++) {
			console.log("We need " + children[childKeys[i]] + " of the " + childKeys[i] + " bags");
			thisBags += (children[childKeys[i]] * countBags(bagParent, childKeys[i]));
		}
		return thisBags;
	} 

	// Get all the outermost bags to loop over
	// For part 2, we always start with the shiny gold bag

	let neededBags = countBags(allBags, "shiny gold");
	
	return neededBags - 1;
}

module.exports = Part2;
