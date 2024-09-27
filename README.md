# Student Matching System

This project implements a system for matching students using optimization techniques. It's designed to create pairings while considering previous matches to avoid repetitions when possible.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Description](#file-description)
- [How It Works](#how-it-works)
- [Setting Up and Running Multiple Times](#setting-up-and-running-multiple-times)
- [Contributing](#contributing)
- [License](#license)

## Features

- Matches students in pairs
- Considers previous matches to avoid repetitions
- Uses optimization techniques to create optimal pairings
- Saves match results for future use

## Requirements

This project requires the following Python libraries:
- pandas (2.2.3)
- amplpy (0.14.0)

This project requires the following licenses:
- [AMPL community editions (free)](https://ampl.com/ce/)
- A [mixed-integer solver](https://ampl.com/products/solvers/open-source-solvers/) (CBC,Highs,etc.), which is used by the AMPL optimization model. CBC and Highs are both sufficient open-source options.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/student-matching-system.git
   cd student-matching-system
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have the solver installed and accessible in your system's PATH, and your AMPL license activated.
   ```
   python -m amplpy.modules install cbc #example
   python -m amplpy.modules activate <your-license-uuid>
   ```

## Usage

1. Prepare your input file:
   - Use `prior_matches.csv` as a template
   - This file should contain a matrix of previous matches (0 for no previous match, 1 for a previous match)

2. Run the matching script:
   ```
   python matching.py
   ```

3. The script will generate a new CSV file (`match_results.csv`) with the updated matches.

## File Description

- `matching.py`: The main Python script that performs the matching
- `requirements.txt`: Lists the required Python packages
- `prior_matches.csv`: Sample input file with no prior matches
- `match_results.csv`: Output file containing the latest matches

## How It Works

1. The system reads the previous match data from `prior_matches.csv`.
2. It uses an AMPL optimization model to create new matches while minimizing repeat pairings.
3. The optimization model considers the following constraints:
   - Each student is matched with exactly one other student
   - Matches are symmetric (if A is matched with B, B is matched with A)
   - The system tries to avoid repeat matches, but allows them if necessary (with a penalty)
4. After solving the optimization problem, the script saves the new matches and prints the results.

## Setting Up and Running Multiple Times

To use the system over time and create multiple sets of matches:

1. Initial Setup:
   - Start with the `prior_matches.csv` file, which contains a matrix of zeros (no prior matches).
   - Ensure all student names are listed correctly in both the first column and first row.

2. First Run:
   - Run the script: `python matching.py`
   - This will generate the first set of matches and save them in `match_results.csv`

3. Subsequent Runs:
   - Before each new run, rename the previous `match_results.csv` to `prior_matches.csv`
   - Run the script again: `python matching.py`
   - The new matches will be saved in `match_results.csv`, considering all previous matches

4. Continuing the Process:
   - Repeat step 3 for each new set of matches you want to create
   - Each time, the system will consider all previous matches to minimize repetitions

Note: If you need to add or remove students between runs, make sure to update the `prior_matches.csv` file accordingly before running the script.

## Handling Odd Number of Students

If you have an odd number of students, you'll need to make some adjustments to ensure everyone is matched. You can do this without modifying the code by adding a "Placeholder" student:

Add a Placeholder Student:
   - Add a "Placeholder" student to your `prior_zeros.csv` or `prior_matches.csv` file (row and column).
   - This placeholder student will be matched with the odd student out in each round.

## Contributing

Contributions to improve the matching system are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request
