import sqlite3


# create_table(table_name, values)
# insert_info(table_name, *values)
# get_info(table_name)
# add_info(name, (value, value), (value, value))


def connect(func):
    def wrapper():
        con = sqlite3.connect('bot_database.db')
        cur = con.cursor()
        func(cur)
        con.commit()
        con.close()

    return wrapper()


def add_table_info(name, lenght, value_names):
    for num in range(0, len(value_names)):
        if num % 2 != 0:
            value_names[num] = ''
    for el in value_names:
        value_names.remove('')
    values = ' '.join(value_names)

    @connect
    def add(cur=None):
        cur.execute('CREATE TABLE IF NOT EXISTS tables_info(name TEXT, lenght INT, value_name TEXT)')
        cur.execute('INSERT INTO tables_info VALUES(?, ?, ?)', (name, lenght, values))


def create_table(name, values):
    @connect
    def create(cur=None):
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {name}({values})""")

    values = values.split(' ')
    lenght = len(values) - 1
    add_table_info(name, lenght, values)


def insert_info(name, values):
    space = ('?,' * len(values))[:-1]

    @connect
    def insert(cur=None):
        cur.execute('INSERT INTO {name} VALUES({space})'.format(name=name, space=space), list(tuple(values)))


def get_info(name):
    values = []

    @connect
    def from_database(cur=None):
        cur.execute(f'SELECT * FROM {name}')
        rec = cur.fetchall()
        for el in rec:

            values.append(el)

    from_database
    return values


def add_info(name, *args):
    def update():
        for el in args:
            insert_info(name, el)
    update()
