import datetime
from flask import redirect, render_template,Flask,jsonify, request,flash
import requests

app = Flask(__name__)
app.secret_key = "test_secret"

@app.route("/",methods=["GET"])
def welcome():
    return render_template("home.html")

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/service",methods=["GET"])
def get_services():
    r = requests.get('http://localhost:8080/post').json()
    return render_template('service.html',posts=r["posts"])

@app.route('/post',methods=["GET", "POST"])
def postHandle():
    if request.method == 'POST':
        post_dict = {
            "title" : request.form.get('title'),
            "details" : request.form.get('details'),
            "category" : request.form.get('category'),
            "author" : "Server",
            "date" : datetime.date.today().strftime("%Y-%m-%d"),
        }
        r = requests.post('http://localhost:8080/post',json=post_dict)
        print(r.json())
        post_id = r.json()['id']
        if post_id :
            return redirect(f'/post/{post_id}')
        else:
            return "failed to create"
    else:
        return render_template('post.html')  
                      
@app.route("/post/<int:id>")
def get_element(id):
    element = requests.get(f"http://localhost:8080/post/{id}").json()
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
    r = requests.delete(f'http://localhost:8080/post/{id}')
    if(r.status_code == 204 ):
        flash('Item Delete Success',"success")
        return redirect('/service')
    else:
        flash('Item Failed to Delete',"danger")
        return redirect('/service')
if __name__ == '__main__':
    app.run(debug=True,port=8000)