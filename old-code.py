cur.execute('''CREATE TABLE IF NOT EXISTS save_settings 
    (id INT AUTO_INCREMENT PRIMARY KEY, in_folder VARCHAR(255), out_folder VARCHAR(255)) ''')


# update folder names
def update_folder(conn, in_folder="none", out_folder="none"):
    cur = conn.cursor()
    try:
        if in_folder == "none":
            cur.execute('''INSERT INTO save_settings VALUES (?,?,?)''', (0, in_folder, out_folder))

        else:
            cur.execute(''' UPDATE save_settings SET in_folder = ?, out_folder = ?  ''', (in_folder, out_folder))
        # Save (commit) the changes
        conn.commit()

    except Error as e:
        print("update folder error ", e)


# get last selected folder value
def get_folders(self):
    cur = self.conn.cursor()
    return cur.execute(''' SELECT * FROM save_settings WHERE id = 0''').fetchall()