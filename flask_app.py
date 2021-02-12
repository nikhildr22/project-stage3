
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memedb.db'
db = SQLAlchemy(app)


class MemeDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime,  default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/memes', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        response = request.get_json()
        # print(response)
        # return jsonify(response['name'])
        name = response['name']
        url = response['url']
        caption = response['caption']
        new_meme = MemeDB(name=name, url=url, caption=caption)

        try:
            db.session.add(new_meme)
            db.session.commit()
            # print(new_meme.id)
            return {"id": new_meme.id}
        except Exception as err:
            print(err)
            return redirect('/')
    else:
        # memes =
        # return render_template("/", memes=memes)
        lis =  MemeDB.query.order_by(desc(MemeDB.date_created)).all()[:100]
        return jsonify([{"id":i.id, "name":i.name ,"url":i.url, "caption":i.caption} for i in lis])

@app.route('/memes/<int:id>')
def meme(id):
    memeId = MemeDB.query.get_or_404(id)

    try:
        return {"id":memeId.id, "name":memeId.name ,"url":memeId.url, "caption":memeId.caption}
    except:
        return "There was a problem deleting the task"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
