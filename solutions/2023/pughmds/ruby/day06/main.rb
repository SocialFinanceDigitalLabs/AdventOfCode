def parse_line(line)
  strings = line.split(" ")
  # Step 2: Filter out non-numeric words
  numeric_words = strings.select { |word| word.match?(/^\d+$/) }
  # Step 3: Convert numeric words to integers
  numeric_words.map(&:to_i)
end

def read_file(file_path)
  begin
    # Read the file synchronously
    data = File.read(file_path, encoding: 'utf-8')

    # Split the content into an array of lines
    lines = data.split("\n")

    # Remove empty lines
    non_empty_lines = lines.reject { |line| line.strip.empty? }

    return non_empty_lines
  rescue StandardError => e
    # kind of like the python try/except function?
    puts "Error reading file: #{e.message}"
    return []
  end
end

def part1(file_path)
  total = 1
  data = read_file(file_path)
  times = parse_line(data[0])
  distances = parse_line(data[1])
  # Pair up the times & distances
  races = times.zip(distances)

  races.each do |time, distance|
    timings = (0...[time, distance + 1].min).to_a
    successes = timings.select { |timing| (time - timing) * timing > distance }

    total *= successes.length
  end

  total
end

def part2(file_path)
  data = read_file(file_path)
  # Combine the numbers together to make a big number, removing spaces
  # Gsub swaps spaces with blanks, and scan looks for numbers in the leftover string
  time_strings = data[0].gsub(/\s+/, '').scan(/\d+/)
  distance_strings = data[1].gsub(/\s+/, '').scan(/\d+/)

  # This may not be needed as I could probably do this on the above definitions. Left here because it works (tm)
  time = time_strings.join('').to_i
  distance = distance_strings.join('').to_i

  # interesting use of the select keyword which Ruby has which works like filter. It will return values based on the
  # condition specified
  successes = (0...[time, distance + 1].min).select { |timing| timing * (time - timing) > distance }
  successes.length
end

file_path = "../../inputs/day06/input.txt"
result = part1(file_path)
puts result
result = part2(file_path)
puts result