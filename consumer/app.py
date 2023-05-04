import datetime
from flask import redirect, render_template,Flask,jsonify, request,flash
import requests
from auth import getTicket


app = Flask(__name__)
app.secret_key = "test_secret"

@app.route("/",methods=["GET"])
def welcome():
    header = getTicket()
    r = requests.get('http://localhost:8080/',headers=header).json()['user']
    return render_template("home.html",user=r)

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/service",methods=["GET"])
def get_services():
    header = getTicket()
    r = requests.get('http://localhost:8080/post',headers=header).json()
    return render_template('service.html',posts=r["posts"])

@app.route('/post',methods=["GET", "POST"])
def postHandle():
    if request.method == 'POST':
        post_dict = {
            "title" : request.form.get('title'),
            "details" : request.form.get('details'),
            "category" : request.form.get('category'),
            "date" : datetime.date.today().strftime("%Y-%m-%d"),
        }
        header = getTicket()
        r = requests.post('http://localhost:8080/post',headers=header,json=post_dict)
        print(r.json())
        post_id = r.json()['id']
        if post_id :
            flash("New Item Created Successfully","success")
            return redirect(f'/post/{post_id}')
        else:
            flash("Failed To Create","danger")
            return redirect(f'/post')
    else:
        header = getTicket()
        r = requests.get('http://localhost:8080/',headers=header).json()['user']
        return render_template('post.html',user=r)  
                      
@app.route("/post/<int:id>")
def get_element(id):
    header = getTicket()
    element = requests.get(f"http://localhost:8080/post/{id}",headers=header).json()
    if element['author'] == "Server" :
        p = "server.jpg"
    else:
        p= 'tommy.jpg'
    if element:
        return render_template('element.html', el=element,img=p)
    else:
        return jsonify({'error': 'Element not found'}), 404

@app.route('/delete/<int:id>')
def delete_element(id):
    header = getTicket()
    r = requests.delete(f'http://localhost:8080/post/{id}',headers=header)
    if(r.status_code == 204 ):
        flash('Item Delete Success',"success")
        return redirect('/service')
    else:
        flash('Item Failed to Delete',"danger")
        return redirect('/service')
if __name__ == '__main__':
    app.run(debug=True,port=8000)