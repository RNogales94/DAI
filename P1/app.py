from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/gatitos.html')
def gatitos():
    return render_template('gatitos.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users/<string>:username')
def profile(username):
    return render_template('profile.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
