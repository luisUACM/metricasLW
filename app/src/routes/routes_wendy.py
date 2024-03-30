from flask import current_app as app
from flask import render_template

@app.route('/dld')
def dld():
    #Aquí va Wendy
    return render_template('dld.html', title='dld', title_long='Densidad de líneas duplicadas')
