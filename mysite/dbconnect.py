import MySQLdb

def connection():
    conn = MySQLdb.connect(host = 'RylonMcnz.mysql.pythonanywhere-services.com',
                           user = 'RylonMcnz',
                           passwd = 'tiptopshop',
                           db = 'RylonMcnz$mydb')

    c = conn.cursor()

    return c, conn