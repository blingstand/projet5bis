import mysql.connector

class DbConnector():
    """class that manage the connection to the database and the fonction related to db"""

    COLUMNS = 'name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags,\
    minerals_tags, palm_oil, composition, link, quantity, brands, nutriments'

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123",
            database="python",
            auth_plugin='mysql_native_password'
        )
        self.my_cursor = self.mydb.cursor()

    def add_substitute(self, name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, palm_oil, composition, link, quantity, brands, nutriments):
        """
        Inserts a line in the table product
        """
        sql = 'INSERT INTO Product ({})'\
        'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}",'\
        ' "{}", "{}");'.format(self.COLUMNS, name, labels, additives, packagings,nutrition_grade, nova_group, traces, \
        manufacturing_places_tags, minerals_tags, palm_oil, composition, link, quantity, brands, nutriments)
        input(sql)
        try:
            self.my_cursor.execute(sql)
            self.mydb.commit() #has to commit the change
            print("-- db good.")
        except Exception as e:
            raise e

