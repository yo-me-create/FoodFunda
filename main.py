from flask import Flask,render_template,request,redirect,session,flash
import mysql.connector as connector
import os

app=Flask(__name__,static_url_path='/static')
app.secret_key=os.urandom(24)#use for session expire

con = connector.connect(
                        host='localhost',
                        port='3306',
                        user='root',
                        password='root',
                        database='myfirstpro'
                        )

cur=con.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cur.execute("SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'".format(email,password))
    users=cur.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        flash("Login successfully > Welcome To Food Funda")
        return redirect ('home')
    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    while True:
        fname=request.form.get('uname')
        lname = request.form.get('ulname')
        email=request.form.get('uemail')
        password=request.form.get('upassword')

        try:
            cur.execute("INSERT INTO `users` (`user_id`,`fname`,`lname`,`email`,`password`) VALUES (NULL,'{}','{}','{}','{}')".format(fname,lname,email,password))

        except:
            flash("Query Error")
        else:
            con.commit()
            flash("Registration successfully > Welcome To Food Funda")

            cur.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
            myuser=cur.fetchall()
            session['user_id']=myuser[0][0]
            return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/additem')
def additem():
    return render_template('/additem.html')

@app.route('/insertitem',methods=['POST','GET'])
def insert():
    if request.method=='POST':
        try:
            product_id=request.form['txtid']
            pname = request.form['txtname']
            catagory = request.form['txtcat']
            price = request.form['txtprice']
            cur.execute("INSERT into items values (%s,%s,%s,%s)",(product_id,pname,catagory,price))
            con.commit()
            flash("insert item successfully > Go to Show Items")
        except:
            flash("We can't insert data")
        finally:
            return render_template('/display.html')


@app.route('/display')
def display():
    cur.execute("Select * from items")
    result=cur.fetchall()
    return render_template('/display.html',result=result)


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        product_id = request.form['textid']
        pname = request.form['txtname']
        catagory = request.form['txtcat']
        price = request.form['txtprice']
        cur.execute("UPDATE items SET pname=%s, catagory=%s, price=%s WHERE product_id=%s", (pname, catagory, price, product_id))
        flash("Data Updated Successfully")
        con.commit()
        return render_template('/display.html')


@app.route('/delete/<string:product_id>', methods = ['GET'])
def delete(product_id):
    cur.execute("DELETE FROM items WHERE product_id=%s", (product_id,))
    con.commit()
    flash("Item has been delete successfully Go to Show items")
    return render_template('/display.html')















#main program
if __name__=="__main__":
    app.run(debug=True)
