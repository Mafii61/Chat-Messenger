from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        
        if not name:
            return render_template("index.html", error="Bitte Namen eingeben")        
        
        return redirect(url_for("chat", name=name))
    return render_template("index.html")
        
@app.route("/chat/<name>", methods=["GET", "POST"])
def chat(name):
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            msg = Message(name=name, content=text)
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for("chat", name=name))

    msgs = Message.query.order_by(Message.created_at).all()
    return render_template("chat.html", name=name, msgs=msgs)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)