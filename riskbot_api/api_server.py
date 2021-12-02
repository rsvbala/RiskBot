from flask import Flask
from flask import jsonify
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 4306
app.config['MYSQL_USER'] = 'abc'
app.config['MYSQL_PASSWORD'] = 'xyz'
app.config['MYSQL_DB'] = 'scap'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # line of code you require
mysql = MySQL(app)

entity_fields = {'ransomware': {'table': 'Malware', 'trending_field': 'lastTrendingOn', 'published_on': 'discoveryTime', 'fields_to_be_fetched': ['name', 'family', 'lastTrendingOn', 'link']},
                 'cve': {'table': 'Cve', 'trending_field': 'cveLastTrendingOn', 'published_on': 'publishedDate', 'fields_to_be_fetched': ['id', 'cveLastTrendingOn', 'publishedDate', 'lastModifiedDate', 'summary']},
                 'exploit': {'table': 'Exploit', 'trending_field': 'lastTrendingOn', 'published_on': 'publishedOn', 'fields_to_be_fetched': ['title', 'description', 'lastTrendingOn', 'subType', 'sourceCode', 'publishedOn', 'modifiedOn']}}


@app.route('/<string:entity>/<string:type>')
def index(entity, type):
    cur = mysql.connection.cursor()
    trending_days = request.args.get('trending')
    published = request.args.get('published')
    size = request.args.get('size')
    size = int(size) if size and int(size) <= 100 else 100
    delta = datetime.datetime.today() - datetime.timedelta(days=int(trending_days if trending_days else 0))
    recent_pub_date = datetime.datetime.today() - datetime.timedelta(days=30)
    if type == 'count':
        fetch = "count(1) as c"
    else:
        fetch = ", ".join(entity_fields.get(entity).get("fields_to_be_fetched"))
    sql = "SELECT {} FROM {} ".format(fetch, entity_fields.get(entity).get("table"))
    if published or trending_days or entity == 'ransomware':
        sql += "WHERE "
    if trending_days:
        sql += " {} >= '{}'".format(entity_fields.get(entity).get("trending_field"), delta)
    if published and trending_days:
        sql += " AND "
    if published:
        sql += " {} >= '{}'".format(entity_fields.get(entity).get("published_on"), recent_pub_date)
    if (published or trending_days) and entity == 'ransomware':
        sql += " AND "
    if entity == 'ransomware':
        sql += " type = 'Ransomware'"
    sql += "ORDER BY id DESC LIMIT {}".format(size)
    print("SQL Query :: {}".format(sql))
    cur.execute(sql)
    if type == 'count':
        data = cur.fetchone()
    else:
        data = cur.fetchall()
    return jsonify(data) # use jsonify here


@app.route('/product/<string:name>')
def product(name):
    cur = mysql.connection.cursor()
    sql = "SELECT group_concat(cve_id) as cves, group_concat(version) as versions, product from CveToCpe WHERE product = '{}' GROUP BY product".format(name)
    cur.execute(sql)
    data = cur.fetchone()
    return jsonify(data)  # use jsonify here


if __name__ == '__main__':
    app.run(debug=True)
