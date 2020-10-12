from flask import Flask, render_template, redirect, request

app = Flask(__name__)

contents = [{'id':1, 'name':"User_A",'suggestion':"Nepalska restavracija",'rating':1},
           {'id':2, 'name':"User_B",'suggestion':"Kitajska restavracija",'rating':1},
           {'id':3, 'name':"User_C",'suggestion':"Mehiška restavracija",'rating':1}]

@app.route('/')
def hello():
    return render_template('list.html', contents=contents)

@app.route('/vote/<int:id>')
def update(id):
    for content in contents:
        if content['id'] == id:
            content['rating'] +=1
    
    return redirect('/')

@app.route('/new', methods=('GET','POST'))
def new_suggestion():
    if request.method == 'POST':
        user_name = request.form['user_name']
        rest_name = request.form['rest_name']
        
        new_sugg = {'id':contents.__len__()+1,
                    'name':user_name,
                    'suggestion':rest_name,
                    'rating':1}
        contents.append(new_sugg)
        return redirect('/')
    
    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True)