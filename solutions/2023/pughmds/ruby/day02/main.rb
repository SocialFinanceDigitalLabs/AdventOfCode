PART_ONE = {
  "red" => 12,
  "green" => 13,
  "blue" => 14
}

def get_phases(row)
  # Don't have to do too much different over the python code
  # Most is roughly the same (except the .to_i function...)
  game_parts = row.split(":")
  game_number = game_parts[0].split(" ")[1].to_i
  phases = game_parts[1].split(";")
  return game_number, phases
end

def part_one(data)
  total = 0
  # Loop over each row
  data.each do |row|
    game_number, phases = get_phases(row)
    game_ok = true

    # Loop over each found phase
    phases.each do |phase|
      groups = phase.strip.split(",")
      # Loop over each group
      groups.each do |group|
        colours = group.strip.split(" ")
        # Check to see if each colour found is within the bounds specified
        if PART_ONE[colours[1]] < colours[0].to_i
          game_ok = false
          break
        end
      end
    end

    # If this row is still good, add the game number to the total
    total += game_number if game_ok
  end

  return total
end


# Specify the file path
file_path = '../../inputs/day02/test1.txt'

# Initialize an empty array to store data
data = []

# Open the file and read its contents into the array
File.open(file_path, 'r') do |file|
  file.each_line do |line|
    data << line.chomp
  end
end

# Run part 1
result = part_one(data)
print "The Answer is: ", result, "\n"