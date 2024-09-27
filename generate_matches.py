import pandas as pd
from amplpy import AMPL

# files to read - EDIT HERE!
prior_match_file = 'prior_matches.csv'
new_match_file = 'match_results.csv' # where to save updated match data for future solutions

# matching code - DO NOT EDIT!

# initialize optimization model
ampl = AMPL()
ampl.eval("reset;")

ampl.eval(
        r"""
            # initialize sets, params, and vars

            set STUDENTS ordered;
            param prior_matches{STUDENTS,STUDENTS};

            var match{STUDENTS,STUDENTS} binary;
            var slack{STUDENTS,STUDENTS} >= 0;

            # constraints

            s.t. one_match_per_student {student in STUDENTS}:
                sum{other in STUDENTS: other != student} match[student,other] = 1;

            s.t. symmetry_constraint {i in STUDENTS, j in STUDENTS: i != j}: 
                match[i,j] = match[j,i];

            s.t. no_repeat_match {student_1 in STUDENTS, student_2 in STUDENTS: student_1 != student_2}:
                prior_matches[student_1,student_2] + match[student_1,student_2] <= 1 + slack[student_1,student_2];

            # objective 

            minimize objective_score: 
                sum{i in STUDENTS, j in STUDENTS: i != j} (0.5 * match[i,j] + slack[i,j]);
            
    """
    )

# load prior match data
prior_matches_df = pd.read_csv(prior_match_file, index_col=0)
STUDENTS_list = prior_matches_df.columns.tolist()
prior_matches_dict = {(i, j): prior_matches_df.loc[i, j] 
                      for i in STUDENTS_list 
                      for j in STUDENTS_list}

# populate model with prior matches data
ampl.set["STUDENTS"] = STUDENTS_list
ampl.param["prior_matches"] = prior_matches_dict

# solve optimization and extract solution
print('solving...')
ampl.solve(solver='cbc') # mixed-integer solver
match_vals = ampl.get_variable("match")

# post processing
def save_and_print_matches(match_var, new_match_file, prior_match_file):
    """
    Extracts, formats, and saves match solution data from model object,
    then prints the matches and statistics.
    """
    # Get the values from the AMPL variable
    match_values = match_var.get_values()
    
    # Convert to a list of tuples
    try:
        data = [(key[0], key[1], value) for key, value in match_values.items()]
    except AttributeError:
        try:
            data = list(match_values)
        except TypeError:
            data = str(match_values).strip().split('\n')[1:]  # Skip header
            data = [line.split() for line in data]
            data = [(d[0], d[1], float(d[2])) for d in data if len(d) == 3]
    
    # Create a DataFrame
    df = pd.DataFrame(data, columns=['student1', 'student2', 'Match'])
    
    # Get unique student names
    STUDENTS = sorted(set(df['student1']) | set(df['student2']))
    
    # Create the final DataFrame
    new_matches_df = pd.DataFrame(0, index=STUDENTS, columns=STUDENTS)
    
    # Fill in the match values
    for _, row in df.iterrows():
        student1, student2, value = row
        new_matches_df.at[student1, student2] = value
    
    # Save new matches to CSV
    new_matches_df.to_csv(new_match_file)
    print(f"\nCSV file '{new_match_file}' has been created.")

    # Read the prior matches
    prior_matches_df = pd.read_csv(prior_match_file, index_col=0)
    
    # Combine new and prior matches
    new_prior_matches_df = new_matches_df + prior_matches_df
    new_prior_matches_df.to_csv(new_match_file)

    print("Matches:")
    new_count = 0
    repeat_count = 0
    
    for i in range(len(new_matches_df.index)):
        for j in range(i+1, len(new_matches_df.columns)):
            if new_matches_df.iloc[i, j] == 1:
                person1 = new_matches_df.index[i]
                person2 = new_matches_df.columns[j]
                
                is_repeat = (prior_matches_df.loc[person1, person2] >= 1) or (prior_matches_df.loc[person2, person1] >= 1)
                match_type = "REPEAT" if is_repeat else "NEW"
                
                print(f"  {person1} - {person2} ({match_type})")
                
                if is_repeat:
                    repeat_count += 1
                else:
                    new_count += 1
    
    total_matches = new_count + repeat_count
    print(f"\nTotal number of matches: {total_matches}")
    print(f"New matches: {new_count}")
    print(f"Repeat matches: {repeat_count}")

save_and_print_matches(match_vals,new_match_file, prior_match_file)