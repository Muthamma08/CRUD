import sqlite3

def connect_to_database(db_path):
    """
    Connect to the SQLite database specified by db_path.
    
    :param db_path: Path to the SQLite database file.
    :return: Connection object to the SQLite database.
    """
    try:
        connection = sqlite3.connect(db_path)
        print(f"Successfully connected to the database at {db_path}")
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

    
def create_table(connection):
    """
    Create a sample table in the SQLite database.
    
    :param connection: Connection object to the SQLite database.
    if table already exists then it doesnt craete new one
    """
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users")  # Clear existing data in the table
        connection.commit()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        connection.commit()
        print("Table 'users' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def insert_user(connection, name, age):
    """
    Insert a new user into the users table.
    
    :param connection: Connection object to the SQLite database.
    :param name: Name of the user.
    :param age: Age of the user.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (name, age) VALUES (?, ?)
        ''', (name, age))
        if cursor.rowcount == 0:
            connection.rollback()
            print(f"Failed to insert user '{name}'.")
        else:
            connection.commit()
            print(f"User '{name}' inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")

def get_data(connection):
    """
    Retrieve and print all users from the users table.
    
    :param connection: Connection object to the SQLite database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        print("Users in the database:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error retrieving data: {e}")

def get_single_user(connection):
    """
    Retrieve and print a single user from the users table.
    
    :param connection: Connection object to the SQLite database.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ?', ("Alice",))
        row = cursor.fetchone()
        if row:
            print("Single user retrieved:")
            print(row)
        else:
            print("No user found with the specified name.")
    except sqlite3.Error as e:
        print(f"Error retrieving single user: {e}")


if __name__ == "__main__":
    db_path = "users.db"
    conn = connect_to_database(db_path)
    print(conn)
    if conn:
        create_table(conn)
        
  
    insert_user(conn, "Alice", 30)
    insert_user(conn,"Mary",25)
    get_data(conn)
    get_single_user(conn)
    conn.close()
