import sqlite3 as sql
con = sql.connect('GlitchDB.db')
c = con.cursor()
# c.execute('create table target_info(target_name text not null , date timestamp , addres text not null, camera blob, audio blob, screen blob,cmd text)')
c.execute('create table target_info(target_name text not null , date text not null, addres text not null)')
con.commit()
con.close()