from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth 配置
oauth = OAuth(app)
oauth.register(
    name='auth_server',
    client_id='FM2JXpo8rIoJwkCy82HHs8uj',  # 在 OAuth 服务器上注册后获得
    client_secret='5Evqf8f3va1quQLXDCJIkvUbKtWY4BopJG6N4zMQkLPjNeUd',  # 在 OAuth 服务器上注册后获得
    access_token_url='http://192.168.1.10:5000/oauth/token',
    authorize_url='http://192.168.1.10:5000/oauth/authorize',
    client_kwargs={'scope': 'profile'},
)


@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.auth_server.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.auth_server.authorize_access_token()
    session['token'] = token
    user = oauth.auth_server.get('http://192.168.1.10:5000/api/me').json()
    session['user'] = user
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect('/')


@app.route('/protected_resource')
def protected_resource():
    if 'token' not in session:
        return redirect(url_for('login'))

    # 使用访问令牌请求受保护的资源
    client = OAuth2Session(
        client_id='your_client_id',
        client_secret='your_client_secret',
        token=session['token']
    )
    response = client.get('http://192.168.1.10:5000/api/me')
    if response.ok:
        return jsonify(response.json())
    else:
        return 'Failed to access protected resource', 403


if __name__ == '__main__':
    app.run(port=8000)
