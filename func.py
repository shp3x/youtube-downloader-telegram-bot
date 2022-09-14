import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


async def db_table_val(user_id: int, link: str):
    cursor.execute('INSERT OR IGNORE INTO main (user_id, link) VALUES (?, ?)', (user_id, link))
    conn.commit()


async def add_link(message):
    sql = "UPDATE main SET link = ? WHERE user_id = ?"
    val = (message.text, message.from_user.id)
    cursor.execute(sql, val)
    conn.commit()


async def clear_link_field(call):
    sql = "UPDATE main SET link = ? WHERE user_id = ?"
    val = ('', call.from_user.id)
    cursor.execute(sql, val)
    conn.commit()
