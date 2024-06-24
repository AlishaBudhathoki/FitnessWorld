import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="FitnessWorld",
    user="postgres",
    password="Storage321@@",
    host="localhost",
    port="5432"
)
c = conn.cursor()

# Insert the user into the users table
c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('Alisha', 'Alisha123@'))
conn.commit()

# Close the database connection
conn.close()
