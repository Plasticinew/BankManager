from flask import render_template

def flash(error_message, action, return_url):
    return render_template(\
        "success.html", action=action,\
        succ=0, showurl=return_url, message=error_message)