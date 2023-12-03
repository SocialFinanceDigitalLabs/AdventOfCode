#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
using namespace std;

std::unordered_map<std::string, int> PART_ONE = {
    {"red", 12},
    {"blue", 13},
    {"green", 14},
};

std::pair<int, std::vector<std::string>> get_phases(const std::string &row) {
    std::istringstream iss(row);
    std::string game_part, phase_part;
    std::getline(iss, game_part, ':');
    int game_number = std::stoi(game_part.substr(game_part.find(' ') + 1));
    std::getline(iss, phase_part);
    std::istringstream phases_ss(phase_part);
    std::vector<std::string> phases;
    while (std::getline(phases_ss, phase_part, ';')) {
        phases.push_back(phase_part);
    }
    return {game_number, phases};
}

std::string trim(const std::string& str) {
    size_t start = 0;
    size_t end = str.length();

    // Find the index of the first non-space character
    while (start < end && std::isspace(str[start])) {
        ++start;
    }

    // Find the index of the last non-space character
    while (end > start && std::isspace(str[end - 1])) {
        --end;
    }

    return str.substr(start, end - start);
}

int run(const std::vector<std::string> &data) {
    int total = 0;

    for (const std::string &row : data) {
        auto [game_number, phases] = get_phases(row);
        bool game_ok = true;

        for (const std::string &phase : phases) {
            std::istringstream groups_ss(phase);
            std::string group_part;

            while (std::getline(groups_ss, group_part, ',')) {

                if (group_part.empty()) {
                    // Skip empty strings
                    continue;
                }

                std::istringstream colours_ss(group_part);
                std::string colour_part;
                std::string count;
                colours_ss >> count >> colour_part;
                colour_part = trim(colour_part);

                try {
                    int int_count = std::stoi(count);
                    if (PART_ONE[colour_part] < int_count) {
                        game_ok = false;
                        break;
                    }
                } catch (const std::invalid_argument& e) {
                    game_ok = false;
                    break;
                }
            }
            if (!game_ok) {
                break;
            }
        }

        if (game_ok) {
            total += game_number;
        }
    }

    return total;
}

int main() {
    // Specify the file path
    std::string file_path = "../../inputs/day02/test1.txt";

    // Initialize an empty vector to store data
    std::vector<std::string> data;

    // Open the file and read its contents into the vector
    std::ifstream file(file_path);
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            data.push_back(line);
        }
        file.close();

        int result = run(data);

        std::cout << "Total: " << result << std::endl;
    } else {
        std::cerr << "Unable to open file: " << file_path << std::endl;
        return 1; // Return an error code
    }

    return 0;
}