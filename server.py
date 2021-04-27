from flask import Flask
from landing import landing
from main import main
from profilepage import profile
from shop import shop
from school import school

app = Flask(__name__)
app.secret_key = 'libervertotopsecretkey'

app.register_blueprint(landing)
app.register_blueprint(main)
app.register_blueprint(profile)
app.register_blueprint(shop)
app.register_blueprint(school)


if __name__ == '__main__':
    app.run(debug=False)
