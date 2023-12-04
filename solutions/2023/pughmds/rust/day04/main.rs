use clap::{App, Arg};
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead, BufReader};


fn parse_card(card: &str) -> (u32, Vec<u32>, Vec<u32>) {
    // Find the position of the colon in "Card 1:"
    let colon_index = card.find(':').unwrap();

    // Extract the card number
    let card_number: u32 = card[5..colon_index].trim().parse().unwrap();

    // Split the string based on the pipe (|) character
    let (left_part, right_part) = card[colon_index + 1..].split_once('|').unwrap();

    // Convert the substrings to vectors of integers
    let winning_numbers: Vec<u32> = left_part
        .split_whitespace()
        .filter_map(|num| num.parse().ok())
        .collect();

    // Let's do the same with the card numbers
    let numbers: Vec<u32> = right_part
        .split_whitespace()
        .filter_map(|num| num.parse().ok())
        .collect();

    // return to the calling function
    (card_number, winning_numbers, numbers)
}

fn run(data: Vec<&str>) -> u32 {
    let mut total = 0;
    for card in data {
        let (_, winning_numbers, numbers) = parse_card(card);

        // A HashSet is the rough equivalent of a python set().  This
        // Collects the numbers into a list of unique values.
        let winning_set: HashSet<_> = winning_numbers.into_iter().collect();
        let numbers_set: HashSet<_> = numbers.into_iter().collect();

        // Find common elements
        let common_elements: HashSet<_> = winning_set.intersection(&numbers_set).cloned().collect();
        if !common_elements.is_empty() {
            total += 2u32.pow((common_elements.len() - 1) as u32);
        }
    }
    total
}

fn run_p2(data: Vec<&str>) -> u32 {
    let mut total = 0;
    let mut cards: Vec<(HashSet<u32>, HashSet<u32>, u32)> = Vec::new();

    for card in data {
        // This time, we need to parse each card separately
        let (_, winning_numbers, numbers) = parse_card(card);
        cards.push((winning_numbers.into_iter().collect(), numbers.into_iter().collect(), 1));
    }

    // Next, we need to create duplicates based on wins
    for index in 0..cards.len() {
        let (win, numbers, _) = &cards[index];

        // Get the winning numbers in the card
        let common_elements: HashSet<_> = win.intersection(numbers).cloned().collect();

        // Count how many and add to the "copies" of the next n cards.
        for n in (index + 1)..(common_elements.len() + index + 1) {
            if n < cards.len() {
                // We win the number of cards again
                cards[n].2 += cards[index].2;
            }
        }
    }

    // Add up the number of cards we have
    for (_, _, copies) in &cards {
        total += *copies;
    }
    total
}


fn main() -> io::Result<()> {
    // Open the file in read-only mode
    let matches = App::new("Your Program")
        .arg(Arg::with_name("input_file").required(true).takes_value(true))
        .get_matches();

    // Retrieve the filename from the command-line arguments
    let filename = matches.value_of("input_file").expect("Input file not provided");

    // Open the file in read-only mode
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    // Collect lines from the file into a Vec<&str>
    // This line reads from the file, and then collects the pieces of the fine into lines
    let data_vec: Vec<String> = reader.lines().filter_map(|line| line.ok()).collect();
    // This line takes the pieces found above, and converts them into strings. I guess vectors in rust are roughly
    // the equivalent of lists?
    let data: Vec<&str> = data_vec.iter().map(|s| s.as_str()).collect();


    let result_part1 = run(data.clone());
    let result_part2 = run_p2(data.clone());

    println!("Result Part 1: {}", result_part1);
    println!("Result Part 2: {}", result_part2);

    Ok(())
}