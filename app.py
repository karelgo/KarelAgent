from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with welcoming message and description."""
    return render_template('home.html')

@app.route('/about')
def about():
    """About page with project description."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)