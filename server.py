from flask import Flask, render_template, Blueprint
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/<int:num>')
def home(num):
   return render_template(f'new{num}.html')
if __name__ == '__main__':
   app.run(debug=True)