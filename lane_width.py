#!\python3\Scripts\python

"""lane_width.py: Given a Road Segment ID, a lane number and a distance from the start of the lane,
return the lane width at that position (you may need to interpolate)"""
__author__ = "Peter Kovacs - 29.04.2021."

try:
    # Import psycopg2 library from virtual-environment
    import sys
    import psycopg2
    from postgr_conn import postgres_connection as pgr# own module
except ModuleNotFoundError as error:
    raise error('No PostgreSQL extension')


# Function: Given a Road Segment ID, a lane number and a distance from the start of the lane, return the lane width at that position
def lane_width(args):

    # PostgreSQL Database Query
    database = "bxfpfzgy"
    cursor = pgr(database)

    sql_query = """SELECT fix_event, lane_width FROM lanes
    INNER JOIN lane_linear_reference ON id = lane_id
    WHERE road_segment_id = {0} AND lane_number = {1}
    ORDER BY fix_event ASC;
    """.format(args[0], args[1])

    # Execute the query and handle the invalid SQL requests.
    try:
        cursor.execute(sql_query)
        pg_result = cursor.fetchall()
        if not pg_result:
            result = "'{0}' Road Segment ID does not exist.".format(args[0])
            return result
    except:
        return "Invalid query"
 
    index, equal = 0, False
    arb_point = int(args[2])

    # Iterate on database response while it finds values for linear interpolation formula
    while (arb_point >= pg_result[index][0]):
        
        # Check if arbitary value is equal to one of fix value, thus it doesnt need interpolation
        if arb_point == pg_result[index][0]:
            width = pg_result[index][1]
            equal = True
            break

        # Store values for interpolation
        lower_event, higher_event = pg_result[index][0], pg_result[index+1][0]
        lower_width, higher_width = pg_result[index][1], pg_result[index+1][1]

        index += 1

    # If equal, it doesnt need interpolation otherwise yes
    if equal:
        return width
    else:
        width = linear_interpolation(arb_point,lower_event, higher_event, lower_width, higher_width)
        return width
        
# Handle input paramaters for bad inputs
def input_handler():

    # Check Road Segment ID validity (not database constraint)
    road_segment_id = input("Enter Road Segment ID: ")
    check_not_string(road_segment_id)

    # Check Lane Number validity (with database constraint)
    lane_number = input("Enter Lane Number: ")
    check_not_string(lane_number)

    # Check database constraint
    if not int(lane_number) in range(-3,4):
        raise NameError('Invalid Lane Number given')
        sys.exit()

    # Check Arbitary point value validity (with database constraint)
    distance_from_start = input("Enter arbitary point to calculate lane-width (m): ")
    check_not_string(distance_from_start)

    # Check database constraint
    if not int(distance_from_start) in range(0,151):
        raise NameError('Invalid Arbitary point length given. It must be beetwwen 0-150')
        sys.exit()

    return road_segment_id, lane_number, distance_from_start

# Check input paramters are not strings
def check_not_string(params):
    try:
        params = int(params)
    except:
        raise NameError('Invalid Parameter given: "{0}" - It must not be string value'.format(params))

# Linear interpolation formula
def linear_interpolation(*args):
    width = (args[0]-args[1])/(args[2]-args[1])*float(args[4]-args[3])+float(args[3])
    return width

# TOP-LEVEL Script environment run the lane_width() function
if __name__ == "__main__":
    result = lane_width(input_handler())
    print(result)
