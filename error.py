from flask import flash

# flash all form error messages
def flash_form_errors(form):
    [ flash(errormsg) for errormsgs in form.errors.values() for errormsg in errormsgs ]
