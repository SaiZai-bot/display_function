import sqlite3

connection = sqlite3.connect('inputs.db')

cursors = connection.cursor()

#create table
cursors.execute("""
CREATE TABLE IF NOT EXISTS Data_Inputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                item TEXT,
                amount TEXT
                      
)
""")
connection.commit()


#insert into database
def saving_to_database(date, category, item, amount):
   
    if date and category and item and amount:
        cursors.execute("""
            INSERT INTO Data_Inputs (date, category, item, amount) VALUES (?,?,?,?)""", (date, category, item, amount))
        
        connection.commit()


def fetch_database():
    connection = sqlite3.connect('inputs.db')
    cursors = connection.cursor()

    cursors.execute("""
        SELECT date, category, item, amount from Data_Inputs""")
    
    data = cursors.fetchall()

    connection.close()

    return data