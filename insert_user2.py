from passlib.hash import bcrypt
import psycopg2

# Hash the password
password = "ananda123@"
hashed_password = bcrypt.hash(password)

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
c.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", ('ananda', hashed_password))
conn.commit()

# Close the database connection
conn.close()
