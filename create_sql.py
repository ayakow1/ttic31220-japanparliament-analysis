import sqlite3

conn = sqlite3.connect('raw_speech.db') 
c = conn.cursor()

c.execute('''
            CREATE TABLE raw_speech (
            id varchar(30),
            house varchar(3),
            committee varchar(30),
            vol varchar(5),
            speech_date date,
            speaker varchar(30),
            party varchar(30),
            speech text,
            morpheme text,
            PRIMARY KEY (id) )
          ''')

# c.execute('''
#             CREATE TABLE speech (
#             id varchar(30),
#             house varchar(3),
#             committee varchar(30),
#             vol varchar(5),
#             speech_date date,
#             speaker varchar(30),
#             party varchar(30),
#             speech text,
#             PRIMARY KEY (id) )
#           ''')
                     
conn.commit()