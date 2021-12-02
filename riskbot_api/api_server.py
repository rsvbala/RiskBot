from flask import Flask
from flask import jsonify
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 4306
app.config['MYSQL_USER'] = 'vbalakrishnan'
app.config['MYSQL_PASSWORD'] = 's1U87nR5xPZDNCCYLUgMHFNqvAoeMq9dAra7Zcy7'
app.config['MYSQL_DB'] = 'scap'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # line of code you require
mysql = MySQL(app)

entity_fields = {'ransomware': {'table': 'Malware', 'trending_field': 'lastTrendingOn', 'fields_to_be_fetched': ['name', 'family', 'lastTrendingOn', 'link']},
                 'cve': {'table': 'Cve', 'trending_field': 'cveLastTrendingOn', 'fields_to_be_fetched': ['id', 'cveLastTrendingOn', 'publishedDate', 'lastModifiedDate', 'summary']},
                 'exploit': {'table': 'Exploit', 'trending_field': 'lastTrendingOn', 'fields_to_be_fetched': ['title', 'description', 'lastTrendingOn', 'subType', 'sourceCode', 'publishedOn', 'modifiedOn']}}


@app.route('/<string:entity>/<string:type>')
def index(entity, type):
    cur = mysql.connection.cursor()
    trending_days = request.args.get('trending')
    size = request.args.get('size')
    size = int(size) if size and int(size) <= 100 else 100
    delta = datetime.datetime.today() - datetime.timedelta(days=int(trending_days if trending_days else 0))
    if type == 'count':
        fetch = "count(1) as c"
    else:
        fetch = ", ".join(entity_fields.get(entity).get("fields_to_be_fetched"))
    sql = "SELECT {} FROM {} ".format(fetch, entity_fields.get(entity).get("table"))
    if trending_days or entity == 'ransomware':
        sql += "WHERE "
    if trending_days:
        sql += " {} >= '{}'".format(entity_fields.get(entity).get("trending_field"), delta)
    if trending_days and entity == 'ransomware':
        sql += " AND "
    if entity == 'ransomware':
        sql += " type = 'Ransomware'"
    sql += "ORDER BY id DESC LIMIT {}".format(size)
    cur.execute(sql)
    if type == 'count':
        data = cur.fetchone()
    else:
        data = cur.fetchall()
    return jsonify(data) # use jsonify here


if __name__ == '__main__':
    app.run(debug=True)
