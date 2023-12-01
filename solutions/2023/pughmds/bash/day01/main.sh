#!/bin/bash
# Could only get part 1 working on this so far...

getDigitsFromString() {
  # Pulls digits from the string
  digits=$(echo "$row" | grep -o '[0-9]')
  # Only uses the first and last digits. The 10# ensures base 10 is being used
  value=$((10#${digits:0:1}${digits: -1}))
  echo "$value"
}

run() {
  # Open the file and read line by line
  while IFS= read -r row || [ -n "$row" ]; do
    value=$(getDigitsFromString "$row")
    # Add up the result from the get digits function
    total=$((total + value))
  done < "$1"
  # return the total from the loop
  echo $total
}

result=$(run "../../inputs/day01/test1.txt")
echo "Result: $result"
