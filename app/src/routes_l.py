from flask import current_app as app
from flask import render_template

@app.route('/McCabe')
def mccabe():
    #Aquí va Luis
    return render_template('mccabe.html', title='Complejidad ciclomática')