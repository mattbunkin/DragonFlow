import os
import json
import pyparsing as pp
from dotenv import load_dotenv
load_dotenv()

# global env that stores location of json data
DATA_FILE = os.getenv("DATA_FILE")


def parse_pre_reqs(user_course: str) -> pp.ParseResults | None:
    """
    ### Organizes a user's pre-reqs in a structured dictionary
        Each entry in the dictionary is from the json file containing
        all courses, algorithm checks at first for pre-reqs; if it finds more 
        pre-reqs inside pre-reqs it makes a new entry in dictionary with
        a recursive approach. Separates each entry by 'or' and 'and' course reqs.
    """

   # define grammar for JSON data. Ex: INFO 212  Minimum Grade: D
    course_id = pp.Word(pp.alphas) + pp.Word(pp.nums)
    # make sure that INFO 212 -> INFO212 (no spaces)
    course_id.setParseAction(lambda tokens: [tokens[0] + tokens[1]])

    grade_req = pp.Literal("Minimum Grade:") + pp.Word(pp.alphas)

    # we take a string and turn each our vocab into a nested list
    course_format = pp.Group(course_id + grade_req)

    # must be leading word and exact match
    keyword_and = pp.Keyword("and")
    keyword_or = pp.Keyword("or")

    # declare the fact we'll use recursive grammar w/ Forward Obj
    expr = pp.Forward()

    # this handles exact expression like: 'course or (any expression within grammar)'
    atom = course_format | pp.Group(pp.Suppress("(") + expr + pp.Suppress(")"))

    # handles any format like: 'A and B and C'; 
    and_expr = atom + pp.ZeroOrMore(keyword_and + atom)

    # handles multiple and expression and multiple or expression with nested and
    expr << and_expr + pp.ZeroOrMore(keyword_or + and_expr)

    # open the json file turn all data into string then into python dict
    with open(DATA_FILE) as data_file:
        course_content = data_file.read()
        course_data = json.loads(course_content)

        # we loop through the json data key and value pairs with the value being the dict
        for crn, pre_req_dict in course_data.items():
            # use string concatenation get course with same subject code and number
            if user_course ==  pre_req_dict["subject_code"]+pre_req_dict["course_number"]:

                # find that same course's pre-reqs 
                user_course_prereqs = pre_req_dict["prereqs"]

                # if there is no pre-reqs return 'None'
                if len(user_course_prereqs) == 0: 
                    return None

                # parse the pre-reqs string
                try:
                    parsed = expr.parseString(user_course_prereqs)
                    return parsed
                
                # print it out to flask server specific error (should never happen)
                except pp.ParseException:
                    # Handle parsing errors
                    print(f"Error parsing pre-reqs for {user_course}")
                

def structure_pre_reqs(all_course_pre_reqs: dict) -> dict:
    # the base case to check if it is a pp.ParseResult then return it
    if not isinstance(all_course_pre_reqs, pp.ParseResults):
        return all_course_pre_reqs
    
    result = []

    for i, item in enumerate(all_course_pre_reqs):
        if isinstance(item, pp.ParseResults):
            # course with grade requirement
            if len(item) >= 3 and item[1] == 'Minimum Grade:':
                result.append({
                    'course': item[0],
                    'grade': item[2]
                })
            else:
                # nested structure
                result.append(structure_pre_reqs(item))
        elif item in ('and', 'or'):
            # Add logical operators
            result.append(item)
        else:
            # Other items
            result.append(item)
    
    return result


def traverse_pre_reqs(parsed_nested_pre_reqs: list, all_course_pre_reqs: dict) -> dict[list]:
    """
    ### Recursively structure each pp.ParseResult object into a structured dictionary
    add the pre-reqs to each entry until len of pre-reqs is 0 

    #### args:
    - parsed_nested_pre_reqs: nested list of pp.ParseResult objects that will be parsed 
    through and added to dictionary with course name as key and the pre-reqs as values
    """

    # iterating through our list that has nested lists
    for pre_req in parsed_nested_pre_reqs:
        # check if it is a nested list (always will be); our base case
        if isinstance(pre_req, pp.ParseResults):
            traverse_pre_reqs(pre_req, all_course_pre_reqs)

        # get to string in nested list w/ course-code and course-num
        else:
            # could be 'min grade' entry.. so try and float convert last 3 chars (course-num)
            try:
                int(pre_req[-3:])
                # store this new nested list of pre_reqs as a value in the course's dict of pre-reqs
                new_pre_req = parse_pre_reqs(pre_req)
                
                # if what should be an messy nested list is empty: go back to top level
                if new_pre_req is None:
                    continue

                # otherwise then simply make a key (w/ pre-reqs name) of its subsequent pre-reqs
                else:    
                    # Convert ParseResults to a cleaner structure before storing into dict
                    clean_prereq = structure_pre_reqs(new_pre_req)
                    all_course_pre_reqs[pre_req] = clean_prereq
                    # this allows us to continue going deeper into the pre-reqs of a pre-req
                    traverse_pre_reqs(new_pre_req, all_course_pre_reqs)

            # if this doesn't work skip entry ('min grade will be skipped')
            except:
                continue
    
    # this takes the first course in the dict and use our function change our entire data structure
    root_course = list(all_course_pre_reqs)[0]
    all_course_pre_reqs[root_course] = structure_pre_reqs(all_course_pre_reqs[root_course])
    
    # we will now return a more and efficient structured dictionary filled with all pre-reqs for a single course
    return all_course_pre_reqs


def can_take_course(
        course_to_check: str, 
        completed_courses: list, 
        all_course_pre_reqs: dict
    ) -> bool:
    """
    ### Determine if a student can take a course based on completed courses and pre-reqs.
    helper function that will be used for the main recursive algorithm that will determine 
    whether or not a user has all the valid pre-reqs

    #### Args:
        - course_to_check: The course code to check eligibility for (ex. structure CS164)
        - completed_courses: List of courses the student has completed (ex. ["CS164", "INFO101"])
        - all_course_pre_reqs: the full structured dict of pre-reqs for a specific course  
    """

    # BC1: course is already completed from user's pre-reqs
    if course_to_check in completed_courses:
        return True
    
    # BC2: course has no pre-reqs in our structure
    if course_to_check not in all_course_pre_reqs:
        return False
    
    # get pre-reqs for this course
    prereqs = all_course_pre_reqs[course_to_check]
    
    # case where there is simply no pre-reqs (empty string)
    if not prereqs:
        return True
    
    # Check the pre-reqs list
    return check_pre_req_list(prereqs, completed_courses, all_course_pre_reqs)


def check_pre_req_list(
        pre_req_list: list, 
        completed_courses: list, 
        all_course_pre_reqs: dict, 
        index: int=0) -> bool:
    """
    ### Recursively check if a list of pre-reqs is satisfied.
    
    #### Args:
        - pre_req_list: list of pre-reqs and logical operators
        - completed_courses: list of courses the student has completed
        - all_course_pre_reqs: structured dict that has a target's course entire pre-reqs
        - index: the index used for iteration specifically in pre-req list for recursion
    """

    # really hard to visualize but this base case works; makes sure we dont surpass list
    if index >= len(pre_req_list):
        return True
    
    current = pre_req_list[index]
    
    # If we have a course requirement
    if isinstance(current, dict) and "course" in current:
        course_code = current["course"]
        
        # Check if the course is completed
        direct_completed = course_code in completed_courses
        
        # If the course is completed, we need to check if its own pre-reqs are satisfied
        if direct_completed:
            prereqs_satisfied = True
            
            # Check if this course has pre-reqs
            if course_code in all_course_pre_reqs:
                course_prereqs = all_course_pre_reqs[course_code]
                if course_prereqs:  # If there are pre-reqs
                    prereqs_satisfied = check_pre_req_list(course_prereqs, completed_courses, all_course_pre_reqs)
            
            # If we're at the end or no operator follows
            if index + 1 >= len(pre_req_list) or not isinstance(pre_req_list[index + 1], str):
                return prereqs_satisfied
            
            # Get the operator
            operator = pre_req_list[index + 1]
            
            if operator == "and":
                # For AND, both sides must be true
                if not prereqs_satisfied:
                    return False
                # Check the rest of the list
                return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 2)
            
            elif operator == "or":
                # For OR, if first condition is true, the whole expression is true
                if prereqs_satisfied:
                    return True
                # Otherwise, check the other side
                return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 2)
        else:
            # If the course is not directly completed, check if its pre-reqs are satisfied
            # which would make it eligible to be taken
            prereqs_satisfied = False
            
            # If the course is in all_course_pre_reqs and has pre-reqs
            if course_code in all_course_pre_reqs and all_course_pre_reqs[course_code]:
                # Check if ALL its pre-reqs are satisfied
                all_prereqs_satisfied = check_pre_req_list(
                    all_course_pre_reqs[course_code], 
                    completed_courses, 
                    all_course_pre_reqs)
                
                # Even if pre-reqs are satisfied, the course itself is not completed
                prereqs_satisfied = False
            
            # If we're at the end or no operator follows
            if index + 1 >= len(pre_req_list) or not isinstance(pre_req_list[index + 1], str):
                return prereqs_satisfied
            
            # Get the operator
            operator = pre_req_list[index + 1]
            
            if operator == "and":
                # For AND, if first condition is false, the whole expression is false
                if not prereqs_satisfied:
                    return False
                # Check the rest of the list
                return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 2)
            
            elif operator == "or":
                # For OR, if first condition is true, whole expression is true
                if prereqs_satisfied:
                    return True
                # Otherwise, check the other side
                return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 2)
    
    # If we have a logical operator
    elif isinstance(current, str) and current in ["and", "or"]:
        # Skip operators, they're handled with the course before them
        return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 1)
    
    # If we have something unexpected, move to the next item
    else:
        return check_pre_req_list(pre_req_list, completed_courses, all_course_pre_reqs, index + 1)

# get course crn via course name
def get_course_crn(course_name: str, find_all=False) -> int:
    """
    ### uses the course name to get the course crn for ML model
    - loops through data file to find the course name inputted by user
    - returns the FIRST instance of a course's CRN

    #### args:
    - string of the course name in subject code and course number format
    ex. "CS164"

    - find_all=True (defaulted at false) but if True this will return a list
    with a specific course's entire CRNs
    """
    with open(DATA_FILE) as data_file:
        course_content = data_file.read()
        course_data = json.loads(course_content)
        
        # empty string until crn found
        course_crn = ""
        
        # store all crns found into list if find_all=True
        course_crns = []
    
        # we loop through the json data key and value pairs with the value being the dict
        for crn, course in course_data.items():
            # use string concatenation get course with same subject code and number
            if course_name ==  course["subject_code"]+course["course_number"]:
                # simply get the crn
                course_crn = int(course["crn"])

                # if you want all crn here it will append value that it found 
                if find_all:
                    course_crns.append(course_crn)
                    continue

    # if our list is empty then raise error where course not found
    if find_all and not course_crns:
        raise LookupError("Course CRNS not found.")
    
    # this case is if find_all == False
    if not find_all and not course_crn:
        raise LookupError("Course CRN not found.")

    if find_all:
        return course_crns
    
    return course_crn
    


def get_crns_info(crns: list[int]) -> list[dict]:
    """
    ### find each json data object associated with each entry of list and store in list pd dictionaries
    - loops through file full of data
    - checks to see if crn in file full of data matches with one of our crns inside our list

    #### args:
    - crns: list of one specific course's entire crns, goal is to get each 
    time slot, lecturer, and any type of data for just one course through
    all of its crns 
    """
    with open(DATA_FILE) as data_file:
        course_content = data_file.read()
        course_data = json.loads(course_content)

        # store one course's entire data in a list of all of its crns data
        crns_data = []
        for our_crn in crns:
            for crn, data in course_data.items():
                # store one the entire data found for one crn in list 
                if int(crn) == our_crn:
                    crns_data.append(data)

    if not crns_data:
        raise LookupError("Could not find any data under these CRNs.")
    
    return crns_data
                


def is_course_available(target_course: str, completed_courses: list) -> bool:
    """
    ### takes a simple target course and completed user pre-reqs list to evaluate if a user is eligible to take course
    - creates structured dictionary of pre-reqs
    - performs all functions to evaluate this 

    #### args:
    - target_course: string of course subject code and subject numbers for ex. "CS164"
    - completed_courses: list of strings that contain same format as user's taken pre-reqs
    """

    # use py parse to initially parse course pre-reqs
    parsed_target_pre_reqs = parse_pre_reqs(target_course)

    # initialize algorithm by setting up our custom data structure
    structured_pre_reqs = {
        target_course: parsed_target_pre_reqs
    }

    # make a 'tree' like structure of ALL of the pre-req's for a course
    all_target_pre_reqs = traverse_pre_reqs(
        parsed_nested_pre_reqs=parsed_target_pre_reqs, 
        all_course_pre_reqs=structured_pre_reqs
    )

    # save boolean value of whether a user can or can't take a course via pre-reqs
    pre_req_eligibility = can_take_course(
        course_to_check=target_course,
        completed_courses=completed_courses,
        all_course_pre_reqs=all_target_pre_reqs
    )

    # set this up so if user doesn't have necessary pre-reqs just stop function 
    if pre_req_eligibility is False:
        return False
    


    return pre_req_eligibility
    


    





# testing functions
if __name__ == "__main__":
    pp_parsed_pre_reqs = parse_pre_reqs("CS277")    
    print(f"Parsed but not structured top-level pre-reqs:{pp_parsed_pre_reqs}\n")

    # put the course in a new dict to contain all pre-reqs 
    structured_pre_reqs = {
        "CS277": pp_parsed_pre_reqs
    }

    all_course_pre_reqs = traverse_pre_reqs(pp_parsed_pre_reqs, structured_pre_reqs)

    # print the pre-reqs for a specific course in ordered 
    for key, value in all_course_pre_reqs.items():
        print(f"The course name: {key}")
        print(f"The course pre-reqs: {value}\n")

    test_cases = [
        ["CS260", "CS270", "MATH221", "CS265"],  # false
        ["CS260", "CS270", "MATH221", "CS265", "ECE105"],  # TRUE
        ["CS260", "CS270", "MATH221", "CS265", "CS172"],  # false
        ["CS260", "CS270", "MATH221", "CS265", "CS172", "CS171"],  # true
    ]

    for course in test_cases:
        print(f"pre-req test case: {course}\nSatisfies: {can_take_course("CS277", course, all_course_pre_reqs)}\n")
    # example usage
    course_crns = get_course_crn(course_name="CS172", find_all=True)
    print(course_crns)

    # only use method for crns list not string of a crn
    course_info = get_crns_info(course_crns)
    for course in course_info:
        print(f"Course info:\n{course}\n")