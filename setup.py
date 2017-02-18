import sqlite3


# Connecting to the database file
conn = sqlite3.connect('ScHoolboy_Queue.sqlite')
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