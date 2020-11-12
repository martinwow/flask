from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///muh_db.db'
db = SQLAlchemy(app)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    suggestion = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<suggestion %r>' % self.id

# contents = [{'id':1, 'name':"User_A",'suggestion':"Nepalska restavracija",'rating':1},
#            {'id':2, 'name':"User_B",'suggestion':"Kitajska restavracija",'rating':1},
#            {'id':3, 'name':"User_C",'suggestion':"Mehiška restavracija",'rating':1}]


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['user_name']
        rest_name = request.form['rest_name']
        new_suggestion = Vote(name=user_name, suggestion=rest_name)

        try:
            db.session.add(new_suggestion)
            # If I want to demonstrate use of app with same starting entries, don't commit, so db is not updated.
            db.session.commit()
            return redirect('/')
        except:
            return "Something went wrong with your database."

    else:
        suggestions = Vote.query.order_by(Vote.id).all()
        return render_template('list.html', contents=suggestions)


@app.route('/upvote/<int:id>')
def upvote(id):
    # Make a query by id; update the rating, commit to db, display in index view
    suggestion = Vote.query.get_or_404(id)

    try:
        suggestion.rating += 1
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue updating the vote."


@app.route('/downvote/<int:id>')
def downvote(id):
    # Make a query by id, change the rating, update the db, display in index view
    suggestion = Vote.query.get_or_404(id)

    try:
        suggestion.rating -= 1
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue updating the vote."


@app.route('/delete/<int:id>')
def delete(id):
    # Make a query, delete, redirect to index view
    deletion = Vote.query.get_or_404(id)

    try:
        db.session.delete(deletion)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting the suggestion.s"


if __name__ == '__main__':
    app.run(debug=True)