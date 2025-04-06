from dotenv import load_dotenv
load_dotenv()

from flask import abort, Flask, redirect, render_template, request, session, url_for
import auth
import os

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.getenv('APP_SECRET')

@app.route("/")
@auth.login_required
def index():
    return render_template('index.html')

app.register_blueprint(auth.bp)

@app.route('/overlay/<user_type>/<int:user_id>')
def show_overlay(user_type, user_id):
    if user_type == "player" or user_type == "camera" or user_type == "commentary":
        return render_template('overlay.html', user_type=user_type, user_id=user_id)
    abort(404)

if __name__ == '__main__':
    app.run(port=os.getenv('SERVER_PORT', os.getenv('PORT', 5000)), host=os.getenv('SERVER_IP', os.getenv('HOST', '127.0.0.1')))    
