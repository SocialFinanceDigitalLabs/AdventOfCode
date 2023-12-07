#!/usr/bin/ruby
# encoding: utf-8

# Second attempt. Had to do searching to figure out.
# This is NOT on my own solution, but one from here: https://shrib.com/#Rhys30YE5PJ
# I added comments to figure it out what was happening.
# This is probably cheating, but my goal this year is to learn.
def parse_input
  categories = {}
  current_category = nil
  seeds = []

  File.readlines('../../inputs/day05/input.txt', chomp: true).each do |line|
    # If the line starts with seeds, these are the initial seed inputs
    if line.start_with?("seeds:")
      puts line
      seed_info = line.split(':')[1].scan(/\d+/).map(&:to_i)
      seeds = []
      seed_info.each_slice(2) {|start,len| seeds << Range.new(start, start+len-1)}
    # Otherwise, look for map to indicate it's a mapping section
    elsif line.end_with?("map:")
      current_category = line.split(' ')[0].gsub('-','_').to_sym
      categories[current_category] = []
    # Finally, if neither, these must be a mapping related to the above category
    else
      dest, source, count = line.scan(/\d+/).map(&:to_i)
      next unless dest
      categories[current_category] << {range: source..(source+count-1), dest: dest}
    end
  end

  # The input is now mapped to the seeds and a category structure for the mapping
  [seeds, categories]
end

def map_category(map, seed)
  new_seeds = []
  map.each do |h|
    range = h[:range]
    dest = h[:dest]
    offset = dest - range.begin

    # This is if the seed isn't in the mapping and should remain the same number
    if seed.end < range.begin || seed.begin > range.end         # no overlap
      next
    end

    # This seed falls within the range, and so the new value is offset
    if seed.begin >= range.begin && seed.end <= range.end       # seed fully in range, all seed maps to 1 new seed
      new_seeds << Range.new(seed.begin+offset, seed.end+offset)
      break
    end

    # I'm not sure what this means, but creates duplicates of the seeds if there's an overlap.
    if seed.begin < range.begin && seed.end > range.end       # range fully inside seed, maps to 3 new seeds
      new_seeds << map_category(map, Range.new(seed.begin, range.begin-1))
      new_seeds << Range.new(range.begin+offset, range.end+offset)
      new_seeds << map_category(map, Range.new(range.end+1, seed.end))
      break
    end


    if seed.begin <= range.begin && seed.end <= range.end       # begin overlap
      new_seeds << Range.new(range.begin+offset, seed.end+offset)
      new_seeds << map_category(map, Range.new(seed.begin, range.begin-1)) if seed.begin < range.begin
      break
    end
    if seed.begin >= range.begin && seed.end >= range.end         # end overlap
      new_seeds << Range.new(seed.begin+offset, range.end+offset)
      new_seeds << map_category(map, Range.new(range.end+1, seed.end)) if seed.end > range.end
      break
    end
  end

  # Sets the resulting seed to the
  new_seeds = [seed] unless new_seeds.size > 0

  # Sets a multi-dimensional array to become a "flat" one-dimensional array, getting rid of nesting
  new_seeds.flatten
end

# Treat seeds as array of Ranges.  Expands to more Ranges as needed by mappings
def find_lowest_location_number(seeds, maps)
  categories = [:seed_to_soil, :soil_to_fertilizer, :fertilizer_to_water, :water_to_light, :light_to_temperature, :temperature_to_humidity, :humidity_to_location]

  categories.each do |category|
    next_seeds = []
    seeds.each do |seed|
      new_seeds = map_category(maps[category], seed)
      next_seeds << new_seeds
    end
    seeds = next_seeds.flatten
  end

  seeds.map(&:begin).min
end

seeds, maps = parse_input

# Find the lowest location number corresponding to any initial seed
lowest_location = find_lowest_location_number(seeds, maps)
puts "Lowest location number: #{lowest_location}"