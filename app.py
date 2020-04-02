from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    fruits= ['Apples', 'kiwi', 'Banana']
    return render_template('index.html', fruits=fruits)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)