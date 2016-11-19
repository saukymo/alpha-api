from utils.dbhelper import DBHelper


class User:

    def __init__(self, form):
        self.name = form.get("name")
        self.age = form.get("age")
        self.gender = form.get("gender") == "Female"
        self.uuid = form.get("uuid")
        self.clinical_id = form.get("clinical_id")
        self.study_id = form.get('study_id')
        self.identification_number = form.get('identification_number')
        self.db = DBHelper()

    def insert(self):
        # INSERT INTO AggregatedData (datenum,Timestamp)
        # VALUES ("734152.979166667","2010-01-14 23:30:00.000")
        # ON DUPLICATE KEY UPDATE
        #   Timestamp=VALUES(Timestamp)
        scripts = """
            INSERT INTO user (`name`, `uuid`, `gender`, `age`, `clinical_id`, `study_id`, `identification_number`)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=%s, gender=%s, age=%s, clinical_id=%s,
            study_id=%s, identification_number=%s;
        """

        connect = self.db.get_connection()
        cursor = connect.cursor()
        cursor.execute(scripts, (self.name, self.uuid, self.gender, self.age, self.clinical_id, self.study_id,
                                 self.identification_number, self.name, self.gender, self.age, self.clinical_id,
                                 self.study_id, self.identification_number))

        connect.commit()
        cursor.close()
        connect.close()


