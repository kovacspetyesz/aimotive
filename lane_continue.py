#!\python3\Scripts\python

"""lane_continue.py: Given a Road Segment ID and a lane number, return the possible next lanes (Road
Segment ID and lane number), where the simulated vehicle can continue its route."""
__author__ = "Peter Kovacs - 29.04.2021."

try:
    # Import psycopg2 library from virtual-environment
    import sys
    import psycopg2
    from postgr_conn import postgres_connection as pgr # own module
except ModuleNotFoundError as error:
    raise error('No PostgreSQL extension')


# Function: Given a Road Segment ID and a lane number, return the possible next lanes (Road Segment ID and lane number), where the simulated vehicle can continue its route.
def lane_continue(args):

    # PostgreSQL Database queries
    database = "bxfpfzgy"
    cursor = pgr(database)

    sql_query = """SELECT next_lane_id FROM lanes
    INNER JOIN lane_connection ON id = lane_id
    WHERE road_segment_id = {0} AND lane_number = {1};
    """.format(args[0], args[1])

    # Execute the query and handle the invalid SQL requests.
    try:
        cursor.execute(sql_query)
        pg_result = cursor.fetchall()
        if not pg_result:
            result = "'{0}' Road Segment ID does not exist or the vehicle can not continue its route.".format(args[0])
            return result
    except:
        return "Invalid query"

    # Get the nex_lane_id = use for the back-select
    next_lane_id = pg_result[0][0]

    # Back-Select, to get the next road-segment & lane number. If database is consistent, here doesnt need to catch wrong db responses
    sql_query = """SELECT road_segment_id, lane_number FROM lanes WHERE id = {0};""".format(next_lane_id)
    try:
        cursor.execute(sql_query)
        pg_result = cursor.fetchall()
        return "Vehicle can can continue its route on {}. Road segment, {}. numbered lane.".format(pg_result[0][0], pg_result[0][1])
    except:
        return "Invalid query"
        
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

    return road_segment_id, lane_number

# Check input paramters are not strings
def check_not_string(params):
    try:
        params = int(params)
    except:
        raise NameError('Invalid Parameter given: "{0}" - It must not be string value'.format(params))

# TOP-LEVEL Script environment run the lane_width() function
if __name__ == "__main__":
    result = lane_continue(input_handler())
    print(result)
