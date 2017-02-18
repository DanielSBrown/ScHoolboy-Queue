import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name1 = 'Room'  # name of the table to be created
table_name2 = 'Song'  # name of the table to be created
new_field = 'ID' # name of the column
field_type = 'text'  # column data type
field_type_2 = 'text'
field_type_3 = 'text'
new_field_2 = 'Systems'
new_field_3 = 'AdminList'
# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('DROP TABLE IF EXISTS Room')
c.execute('CREATE TABLE Room (ID text, Systems text, AdminList text)')
        #.format(tn=table_name1, nf=new_field, ft=field_type, nf2=new_field_2, ft2=field_type_2, nf3=new_field_3, ft3=field_type_3))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('DROP TABLE IF EXISTS Song')
c.execute('CREATE TABLE Song (Current text, Next text)')
       # .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()