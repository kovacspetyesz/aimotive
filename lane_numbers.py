#!\python3\Scripts\python

"""lane_numbers.py: Given a Road Segment ID, return the number of lanes in both directions"""
__author__ = "Peter Kovacs - 29.04.2021."

try:
    # Import psycopg2 library from virtual-environment
    import psycopg2
    from postgr_conn import postgres_connection as pgr# own module
except ModuleNotFoundError as error:
    raise error('No PostgreSQL extension')

# Road Segment ID - input parameter, check is it integer?
road_segment_id = input("Enter Road Segment ID: ")
try:
    road_segment_id = int(road_segment_id)
except:
    raise NameError('Invalid Parameter given: "{0}" - It must not be string value'.format(road_segment_id))

# Function: Given a Road Segment ID, return the number of lanes in both directions
def lane_numbers(road_segment_id):

    # PostgreSQL Database query
    database = "bxfpfzgy"
    cursor = pgr(database)
    sql_query = "SELECT lane_number FROM lanes WHERE road_segment_id ={0};".format(road_segment_id)

    # Execute the query and handle the invalid SQL requests.
    try:
        cursor.execute(sql_query)
        pg_results = [lane[0] for lane in cursor.fetchall()]
        if pg_results:
            result = ','.join(str(lane) for lane in pg_results)
            return result
        else:
            result = "'{0}' Road Segment ID does not exist.".format(road_segment_id)
            return result

    except:
        return "Invalid query"

# TOP-LEVEL Script environment run the lane_numbers() function
if __name__ == "__main__":
    result = lane_numbers(road_segment_id)
    print(result)
