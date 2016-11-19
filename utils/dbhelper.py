import pymysql
import configparser


class DBHelper:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read('configs/dev.ini')

        connect_string = {}
        for option in cf.options('mysqld'):
            connect_string[option] = cf.get('mysqld', option)
        connect_string['port'] = int(connect_string['port'])
        self.connect_string = connect_string

    def get_connection(self):
        return pymysql.connect(**self.connect_string)

    def prepare_database(self):
        scripts = ["""CREATE TABLE IF NOT EXISTS `history`
                    (
                        `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        `type` VARCHAR(20) NOT NULL,
                        `filename` VARCHAR(50) UNIQUE NOT NULL,
                        `uuid` VARCHAR(50) NOT NULL,
                        `create_time` VARCHAR(50) NOT NULL,
                        `rating` INT NOT NULL,
                        `doctor` VARCHAR(50) NOT NULL,
                        `clinical_status` INT NOT NULL,
                        `pd_medicine` INT NOT NULL,
                        `dopamine` INT NOT NULL
                    ) DEFAULT CHARACTER SET utf8
                    DEFAULT COLLATE utf8_general_ci;""",
                   """CREATE TABLE IF NOT EXISTS `user`
                    (
                        `id` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        `name` VARCHAR(20) NOT NULL,
                        `uuid` VARCHAR(50) UNIQUE NOT NULL,
                        `age` INT NOT NULL,
                        `gender` INT NOT NULL,
                        `clinical_id` VARCHAR(20) NOT NULL,
                        `study_id` VARCHAR(20) NOT NULL,
                        `identification_number` VARCHAR(20)
                    )DEFAULT CHARACTER SET utf8
                    DEFAULT COLLATE utf8_general_ci;"""]

        connection = self.get_connection()
        cursor = connection.cursor()

        for script in scripts:
            cursor.execute(script)
        connection.commit()

        cursor.close()
        connection.close()
