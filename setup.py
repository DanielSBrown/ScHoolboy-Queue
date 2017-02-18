import sqlite3


# Connecting to the database file
conn = sqlite3.connect('ScHoolboy_Queue.sqlite')
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('DROP TABLE IF EXISTS Room')
c.execute('CREATE TABLE Room (ID text, Systems text, AdminList text)')

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('DROP TABLE IF EXISTS Song')
c.execute('CREATE TABLE Song (Current text, Next text)')


c.execute("INSERT INTO ROOM (ID, Systems, AdminList) VALUES ('JKLO', 'Danny''s iPhone', 'Danny');")
c.execute("INSERT INTO Song (Current, Next) VALUES ('Dark Horse', 'Bound 2')")
# Committing changes and closing the connection to the database file
conn.commit()
conn.close()