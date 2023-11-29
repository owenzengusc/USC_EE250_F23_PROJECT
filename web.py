from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/image/<filename>')
def image(filename): 
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()
