import uuid
import gradio as gr


def register_valid_user():
    _users = [
        {"user":"nero", "passwd":"964", "ak":"4ee63915-ab56-456f-b809-1dd2bfb24655"},
        {"user":"bill", "passwd":"425", "ak":"b7933e5c-7a36-45a9-883d-643182b1008c"},
    ]
    return _users


def valid_users():
    items = register_valid_user()
    users = {}
    for user in items:
        users[user["user"]] = user
    return users

def check_login(user="", passwd=""):
    users = valid_users()

    item = users.get(user, None)
    if not item:
        return '<h2 style="color: red;">username not exists</h2>', "", ""
    if item["passwd"] != passwd:
        return '<h2 style="color: red;">password error</h2>', "", ""

    ak = item.get("ak", None)
    if ak is not None:
        return f'<h2 style="color: limegreen;">{user} login</h2>', user, ak
    else:
        ak = str(uuid.uuid4())
        # refresh access key to db

    return f'<h2 style="color: limegreen;">{user} login</h2>', user, ak

def check_cookie(request: gr.Request):
    user, ak = _check_cookie(request)
    if not user:
        return '<h2>None login</h2>', user, ""
    return f'<h2 style="color: limegreen;">{user} login</h2>', user, ak


def _check_cookie(request: gr.Request):
    users = valid_users()
    cookie_ak = request.request.cookies.get("ak", None)
    if not cookie_ak:
        return None, ""

    for user,item in users.items():
        ak = item.get("ak", "")
        if ak == cookie_ak:
            return user, ak
    return None, ""

