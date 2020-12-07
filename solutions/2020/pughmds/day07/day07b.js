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
	// Part 1 used kind of a bad hybrid recursion. This is fully recursive.
	function countBags(bagParent, child) {
		// We need to keep track of the children (how many bags are inside)
		const children = allBags[child].innerTypes;
		// And the keys (what bags are inside)
		const childKeys = Object.keys(children);

		// I had to make this 1 to start with.
		let thisBags = 1;

		// Only count this bag as there is nothing inside
		if (children.length === 0) {
			return 1; 
		}
	
		// Use recursion to look in the bags we've found in the contents
		for (let i = 0; i < childKeys.length; i++) {
			// We multiply the number of bags listed, with the number INSIDE those bags
			thisBags += (children[childKeys[i]] * countBags(bagParent, childKeys[i]));
		}
		return thisBags;
	} 

	// Get all the outermost bags to loop over
	// For part 2, we always start with the shiny gold bag

	let neededBags = countBags(allBags, bagToLookFor);
	
	// Because I started with 1, my results were always off by 1.  I could probably do this more elegantly, but I'll just subtract here
	return neededBags - 1;
}

module.exports = Part2;
