#!/bin/bash

# Set what we expect
red_cubes=12
green_cubes=13
blue_cubes=14
total=0

run() {
  # Open the file and read line by line
  while IFS= read -r row || [ -n "$row" ]; do
    # Assume everything is good to start
    row_ok=1
    # Get the game number from the string
    game_number=$(echo "$row" | grep -oP 'Game \K\d+')
    # Ignoring the game number, split the rest of the string by semicolon (parts)
    IFS=';' read -ra parts <<< "$(echo "$row" | sed 's/Game [0-9]\+: //')"
    for part in "${parts[@]}"; do
      # Split each part into number / color pairs
      IFS=',' read -ra colours <<< "$part"
      for colour in "${colours[@]}"; do
        IFS=' ' read -r number colour_name <<< "$colour"
        # Now, we can check to see if each value fetched is larger than what's possible
        if [ "$colour_name" == "blue" ] && [ "$number" -gt "$blue_cubes" ]; then
          row_ok=0
        elif [ "$colour_name" == "green" ] && [ "$number" -gt "$green_cubes" ]; then
          row_ok=0
        elif [ "$colour_name" == "red" ] && [ "$number" -gt "$red_cubes" ]; then
          row_ok=0
        fi
      done
    done
    # Each time we detect a row that is possible, add the game number to the total
    if [ "$row_ok" == 1 ]; then
      ((total+=$game_number))
    fi
  done < "$1"
  # return the total from the loop
  echo $total
}



#result=$(run "../../inputs/day02/test5.txt")
result=$(run "../../inputs/day02/input.txt")
echo "Result: $result"