import psycopg2
from psycopg2 import Error
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class myDB():
    def __init__(self,dd):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                          password="alim",
                                          host="127.0.0.1",
                                          port="5432",
                                          database=dd)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            self.cursor = self.connection.cursor()

        except (Exception, Error) as error:
            h = 2
#            print("Ошибка при работе с PostgreSQL", error)
        finally:
            h = 1
#            print("Соединение с PostgreSQL закрыто")

    def query(self, q):
        self.cursor.execute(q)
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def callproc(self, func, params):
        return self.cursor.callproc(func, params)



db = myDB('py1')

postgresql_func = """
CREATE OR REPLACE FUNCTION filter_by_priqq(max_price integer)
  RETURNS TABLE(id char(3), model TEXT, price TEXT, rrr INT) AS $$
BEGIN
 RETURN QUERY
 select * from lab1.ship;
END;
$$ LANGUAGE plpgsql;
"""
db.query(postgresql_func)

db.query('drop database py5')
db.query('create database py5')
db.connection.close()

db = myDB('py5')
db.query(postgresql_func)
db.callproc('filter_by_priqq',[999,])


db.query('select 1')
result = db.fetchall()
for row in result:
    print("Id = ", row[0], )



db.callproc('filter_by_priq',[999,])


result = db.fetchall()
for row in result:
    print("Id = ", row[0], )
    print("Model = ", row[1])
    print("Price  = ", row[2])











    def create(self):
        self.table1 = table_model.TableViewWindow()




        ok = uid.myshow()
        if ok:
            uid.myshow()

    def showDialog(self):
        ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')







#    DWindow = QtWidgets.QDialog()
#    uid = createdb.CreateDBWin()
#    uid.setupUi(DWindow)
#    ui.pushButton.clicked.connect(uid.myshow)

#    MainWindow.show()