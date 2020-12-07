const Part1 = (rulesText, bagToLookFor) => {
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
  	let validBags = new Set();

	function findBags(child, bagParent, bagToLookFor) {
		const children = Object.keys(allBags[child].innerTypes);

		// Look through the contents for our bag
		if (children.includes(bagToLookFor)) {
			validBags.add(bagParent);
			return;
		}

		if (children.length === 0) {
			return;
		}
	
		// Use recursion to look in the bags we've found in the contents
		for (let i = 0; i < children.length; i++) {
			findBags(children[i], bagParent, bagToLookFor);
		}
	} 

	// Get all the outermost bags to loop over
	const mainBags = Object.keys(allBags);

	for (let i = 0; i < mainBags.length; i++) {
		// Search for our bag to find
		findBags(mainBags[i], mainBags[i], bagToLookFor);
	}

	return validBags.size;
}

module.exports = Part1;
