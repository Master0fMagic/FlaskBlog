from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
#https://git.heroku.com/flas-blog.git
#creating server
app=Flask(__name__)
app.secret_key="it is a secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    intro=db.Column(db.String(300), nullable=False)
    title=db.Column(db.String(100), nullable=False)
    text=db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

#отслеживание url
@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/help")
@app.route("/about")
@app.route("/info")
def about():
    return render_template("about.html")


@app.route("/user/<string:name>/<string:id>")
def user(name,id):
    return f"User {name}, ID N {id} is You."


@app.route("/sing-in")
def sing_In():
    return render_template("sing-in.html")


@app.route("/posts")
def posts():
    #первая запись из бд .first()
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>", methods=["GET", "POST"])
def show_post(id):
    article=Article.query.get(id)
    return render_template("post.html",article=article)
    

@app.route("/posts/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    article=Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return render_template("operation-successful.html", message="Статья успешно удалена!")
    except Exception as e:
        print(e)
        return render_template("operation-failed.html", message="Во время удаления статьи произошла ошибка.")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'])
def update_article(id):
    article=Article.query.get(id)
    
    if request.method =="POST":
        if request.form['title'] == "" or request.form['text'] == "" or request.form['intro'] == "":
            flash("Заполните все поля",category="error")
            return render_template("article-update.html", article=article)

        article.title=request.form['title']
        article.text=request.form['text']
        article.intro=request.form['intro']
        
        try:
            db.session.commit()
            return render_template("operation-successful.html", message="Статья успешно изменена!")
        except Exception as e:
            print(e)
            return render_template("operation-failed.html", message="Во время редактирования статьи произошла ошибка.")
    else:
        return render_template("article-update.html", article=article)


@app.route("/create-article", methods=['POST', 'GET'])
def create_article():
    if request.method =="POST":
        title=request.form['title']
        text=request.form['text']
        intro=request.form['intro']
        if title=="" or text=="" or intro=="":
            flash("Заполните все поля",category="error")
            return render_template("create_article.html")
        article=Article(title=title,text=text,intro=intro )
        
        try:
            db.session.add(article)
            db.session.commit()
            return render_template("operation-successful.html", message="Статья успешно добавлена!")
        except Exception as e:
            print(e)
            return render_template("operation-failed.html", message="Во время создания статьи произошла ошибка")
    else:
        return render_template("create_article.html")

if __name__ =="__main__":
    app.run(debug=True)