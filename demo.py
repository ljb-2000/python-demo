import MySQLdb as mysql
from flask import Flask,request,render_template,session, redirect,url_for
app = Flask(__name__)
con = mysql.connect(user='root',\
                    passwd='',\
                    db='winiu4',\
                    host='localhost',
                    charset = "utf8")
con.autocommit(True)
cur = con.cursor()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/loginaction')
def loginaction():
    if request.args.get('username')=='51reboot' and request.args.get('password')=='51reboot':
        session['username'] = '51reboot'
    return redirect(url_for('index'))
# idc
@app.route('/idc')
def idc():
    if 'username' not in session:
        return redirect(url_for('login'))
    sql = 'select * from idc'
    cur.execute(sql)    
    return render_template('idc.html',data=cur.fetchall())

@app.route('/addidc')
def addidc():
    if 'username' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name')
    msg = request.args.get('msg')
    sql = 'insert into idc (name,msg) values ("%s","%s")' % (name,msg)
    cur.execute(sql)
    return 'ok'
@app.route('/deleteidc')
def deleteidc():
    if 'username' not in session:
        return redirect(url_for('login'))
    delete_id = request.args.get('id')
    sql = 'delete from idc where id = %s' % (delete_id)
    cur.execute(sql)
    return 'ok'


@app.route('/mac')
def mac():
    if 'username' not in session:
        return redirect(url_for('login'))
    sql = 'select * from mac'

    sql_idc = 'select * from idc'
    if request.args.get('idc'):
        sql = sql+' where idc_id = "'+request.args.get('idc')+'"'
    print sql
    cur.execute(sql_idc)
    idc_data = cur.fetchall()
    cur.execute(sql)    
    return render_template('mac.html',data=cur.fetchall(),idc_data=idc_data)

@app.route('/addmac')
def addmac():
    if 'username' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name')
    ip = request.args.get('ip')
    port = request.args.get('port')
    idc_id = request.args.get('idc_id')
    disk = request.args.get('disk')
    
    sql = 'insert into mac (name,ip,port,idc_id,disk) values ("%s","%s","%s","%s","%s")' % (name,ip,port,idc_id,disk)
    print sql
    cur.execute(sql)
    return 'ok'
@app.route('/deletemac')
def deletemac():
    if 'username' not in session:
        return redirect(url_for('login'))

    delete_id = request.args.get('id')
    sql = 'delete from mac where id = %s' % (delete_id)
    cur.execute(sql)
    return 'ok'





@app.route('/list')
def list():
    init_str = ''
    sql = 'select * from cmdb'
    cur.execute(sql)
    for c in cur.fetchall():

        init_str = init_str + '''<tr><td>%s</td><td>%s</td><td>
                                <button data-id="%s" class="btn btn-warning delete">
                                delete</button>
                                <button data-id="%s" class="btn btn-info update">
                                update</button>
                                </td></tr>''' % (c[1],c[2],c[0],c[0])
    print init_str
    return init_str

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    sql = 'select count(*) from idc'
    cur.execute(sql)
    idc_num = cur.fetchall()[0][0]
    sql_mac = 'select count(*) from mac'
    cur.execute(sql_mac)
    mac_num = cur.fetchall()[0][0]
    return render_template('index.html',idc_num=idc_num,mac_num=mac_num)
    

@app.route('/delete')
def delete():
    delete_id = request.args.get('id')
    sql = 'delete from cmdb where id = %s' % (delete_id)
    cur.execute(sql)
    return 'ok'
@app.route('/search')
def search():
    id = request.args.get('id')
    sql = 'select memory from cmdb where id = %s' % (id)
    cur.execute(sql)

    return str(cur.fetchall()[0][0])
@app.route('/update')
def update():
    id = request.args.get('id')
    memory = request.args.get('memory')
    sql = 'update cmdb set memory=%s where id = %s' % (memory,id)
    cur.execute(sql)
    return 'ok'

@app.route('/add')
def add():
    server = request.args.get('server')
    memory = request.args.get('memory')
    sql = 'insert into cmdb (server,memory) values ("%s",%s)' % (server,memory)
    cur.execute(sql)
    return 'ok'




if __name__ == '__main__':
    app.run(debug=True,port=9092,host='0.0.0.0')







