#!/bin/bash

input_file="../../inputs/day06/input.txt"

# -------------PART 1-------------
# Gives correct answer

# Read the contents of the file into variables
time_line=$(sed -n '1p' $input_file)
distance_line=$(sed -n '2p' $input_file)

# Extract numeric values from the lines
time_values=($(echo "$time_line" | grep -oE '[0-9]+' | tr '\n' ' '))
distance_values=($(echo "$distance_line" | grep -oE '[0-9]+' | tr '\n' ' '))

echo "I: ${time_values[@]}"

total=1

for ((i = 0; i < ${#time_values[@]}; i++)); do
  time=${time_values[$i]}
  distance=${distance_values[$i]}
  successes=0

  timings=($(seq 0 $((time < distance ? time : distance))))

  for current_timing in "${timings[@]}"; do
    if [ $((current_timing * (time - current_timing))) -gt $distance ]; then
      ((successes++))
    fi
  done

  if [ $successes -gt 0 ]; then
    ((total *= successes))
  fi
done

echo "Total (Part 1): $total"


