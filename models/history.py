from utils.dbhelper import DBHelper


class History:

    def __init__(self, form, filename):
        self.history_type = form.get("type")
        self.filename = filename
        self.user_uuid = form.get("uuid")
        self.create_time = form.get("date")
        self.rating = form.get("rating")
        self.doctor = form.get("doctor")
        self.clinical_status = form.get("clinical_status") == "true"
        self.pd_medicine = form.get("pd_medicine") == "true"
        self.dopamine = form.get("dopamine")
        self.db = DBHelper()
        print(form)

    def insert(self):
        scripts = """
            INSERT INTO history (`type`, `filename`, `uuid`, `create_time`, `rating`, `doctor`,
            `clinical_status`, `pd_medicine`, `dopamine`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE type = %s;
        """

        connect = self.db.get_connection()
        cursor = connect.cursor()
        print(scripts)
        cursor.execute(scripts, (self.history_type, self.filename, self.user_uuid,
                                 self.create_time, self.rating, self.doctor, self.clinical_status, self.pd_medicine,
                                 self.dopamine, self.history_type))

        connect.commit()
        cursor.close()
        connect.close()

    @staticmethod
    def get_all_histories():
        scripts = """
           SELECT * FROM history LEFT JOIN user ON history.uuid = user.uuid;
        """

        db = DBHelper()
        connect = db.get_connection()
        cursor = connect.cursor()
        cursor.execute(scripts)

        result = cursor.fetchall()
        print(result)

        return result
