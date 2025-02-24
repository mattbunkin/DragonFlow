def parse_pre_reqs(user_course: str, course_data: dict) -> dict | None:
    """
    Organizes a user's pre-reqs in a structured dictionary
        Each entry in the dictionary is from the json file containing
        all courses, algorithm checks at first for pre-reqs; if it finds more 
        pre-reqs inside pre-reqs it makes a new entry in dictionary with
        a recursive approach. Separates each entry by OR and AND course reqs.
    """

    pre_reqs = {}

    for course in course_data:

        # use string concatenation get course with same subject code and number
        if user_course == course["subject_code"]+course["course_number"]:
            
            # find that same course's pre-reqs 
            user_course_prereqs = course["prereqs"]

            # if there is no pre-reqs return 'None'; base case 
            if len(user_course_prereqs) == 0: 
                return None

            # add spaces between splits to avoid spaces in list elements
            user_course_prereqs = user_course_prereqs.split(" or ")

            # gets courses WITH 'and' pre-req requirements 
            and_prereqs = [course for course in user_course_prereqs if "and" in course]
            
            # parse through the list of 'and' courses make it a string again to get rid of unnecessary words in string
            and_prereqs = str("".join(and_prereqs)).split(" and ")

            # get rid of any entry in the list that has 'and' inside it; pure 'or' pre-reqs
            or_prereqs = [course for course in user_course_prereqs if "and" not in course]



    


def confirm_course(user_prereqs: list, course: dict) -> True | False:
    """
    Perform a backward graph traversal (through parsed pre-reqs dict)
    to confirm whether or not course is inside or not.
        - Each course is a node
        - A pre-req connected to a course is an edge 
        - Returns True if user has a valid prereqs
    """
