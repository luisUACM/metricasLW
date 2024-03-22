from flask import current_app as app
from flask import render_template

@app.route('/LIM')
def lim():
    #Aquí va Wendy
    return render_template('lim.html', title='LIM')
