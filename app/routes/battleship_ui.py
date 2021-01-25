from flask import render_template, current_app as app

@app.route('/battleship/vue')
def vue_view():
    return render_template("battleship/vue_view.html")
