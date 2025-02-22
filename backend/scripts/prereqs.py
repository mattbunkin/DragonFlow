x = "CS 172 Minimum Grade: C or ECE 105 Minimum Grade: D or ECEC 201 Minimum Grade: D CS 260  Minimum Grade: C and CS 270  Minimum Grade: C and MATH 221  Minimum Grade: C"
y = x.split(" or ")

# gets courses WITH and.. 
z = [course for course in y if "and" in course]
print(z)

# push z into something i dont know

# graph traversal approach


"""
Pre-Req Check
- Each course is a node
- Pre-reqs are directed edges pointing from the pre-reqs of course
- Use this function to parse strings into structured format
"""

def parse_pre_reqs(course):
    pass


def confirm_course(course):
    pass