require 'set'
# First attempt: worked great for part 1, but too slow for part 2 (it'd take 3.5 days to get an answer on my
# really old personal computer). This is a brute-force method. It'd get the job done, but take forever. There
# are faster ways to do this, such as using the mapping functions.

def parse_maps(maps)
  map_pipe = {}

  maps.each_with_index do |map_values, i|
    values = map_values.split("\n")[1..]
    map_pipe[i] ||= []

    values.each do |map_val|
      next if map_val.empty?

      input_data = map_val.split.map(&:to_i)
      drs, srs, rl = input_data
      map_pipe[i] << { "dest_range_start" => drs, "source_range_start" => srs, "range_length" => rl }
    end
  end

  map_pipe
end

def parse_input(data)
  instructions_text = data.join("\n")
  sections = instructions_text.split(/\n\s*\n/)
  seeds = sections[0].split(":")[1].strip.split.map(&:to_i)
  processes = []

  sections[1..].each do |sect|
    process = []
    seed_data = sect.split(":")[1].strip.split("\n")

    seed_data.each do |item|
      seed_strings = item.strip.split.map(&:to_i)
      process << seed_strings
    end

    processes << process
  end

  [seeds, processes]
end

def part_one(data)
  seeds, processes = parse_input(data)
  seeds = Set.new(seeds)
  result = []

  seeds.each do |seed|
    processes.each do |step|
      step.each do |process|
        diff = process[0] - process[1]

        if (process[1]..(process[1] + process[2] - 1)).cover?(seed)
          seed += diff
          break
        end
      end
    end

    result << seed
    puts result
  end

  result.min
end

def part_two(data)
  seeds, processes = parse_input(data)
  seeds = seeds.each_slice(2).to_a
  min_loc = Float::INFINITY

  seeds.each do |seed_group|
    start_seed, range_length = seed_group
    puts start_seed
    (start_seed..(range_length + start_seed - 1)).each do |i|
      r = i

      processes.each do |step|
        step.each do |process|
          diff = process[0] - process[1]

          if (process[1]..(process[1] + process[2] - 1)).cover?(r)
            r += diff
            break
          end
        end
      end
      min_loc = [min_loc, r].min
    end
  end

  min_loc
end






# Specify the file path
file_path = '../../inputs/day05/input.txt'

# Initialize an empty array to store data
data = []

# Open the file and read its contents into the array
File.open(file_path, 'r') do |file|
  file.each_line do |line|
    data << line.chomp
  end
end

# Run part 1
#result = part_one(data)
#print "The Part 1 Answer is: ", result, "\n"

# Run part 2
result = part_two(data)
print "The Part 2 Answer is: ", result, "\n"