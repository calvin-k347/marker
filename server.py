from flask import Flask, render_template, Blueprint
app = Flask(__name__)

@app.route('/<num>')
def home(num):
   return render_template(f'new{num}.html')
if __name__ == '__main__':
   app.run(debug=True)