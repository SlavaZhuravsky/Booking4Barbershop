import sqlite3
from aifc import Error

#PRIMARY KEY
class SQLighter:
    ql_create_tasks_table = """CREATE TABLE IF NOT EXISTS clients (
                                        user_id integer,
                                        client_name text NOT NULL,
                                        date text NOT NULL,
                                        _time text NOT NULL,
                                        service_type text NOT NULL,
                                        status bool NOT NULL
                                    );"""

    def __init__(self, database):
        # connect to DB & save cursor connection
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            self.connection.execute(self.ql_create_tasks_table)
        except Error as e:
            print(e)

    def get_booked_time(self, check_date):
        # Get all active bot followers
        with self.connection:
            return self.cursor.execute('SELECT _time FROM `clients` WHERE `status` = 1 AND `date` = ?', (check_date,))\
                .fetchall()

    def subscriber_exists(self, user_id):
        # Check user in DB
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_client(self, user_id, client_name, date, _time, service_type, status=True):
        # add new follower
        with self.connection:
            return self.cursor.execute("INSERT INTO `clients` (`user_id`, `client_name`, `date`, `_time`, "
                                       "`service_type`, `status`) "
                                       "VALUES( ""?,?,?,?,?,?)", (user_id, client_name, date, _time, service_type, status))

    def delete_client(self, user_id):
        sql = 'DELETE FROM clients WHERE user_id=?'
        self.connection.execute(sql, (user_id,))

    def remove_client(self, user_id):
        # Update user subscribe status
        with self.connection:
            return self.delete_client(user_id)

    def close(self):
        # Close DB connection
        self.connection.close()
