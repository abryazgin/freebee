from flask import Blueprint, request
from actioner import BaseActioner, RequestException
import actioner

app_api = Blueprint('api', __name__)


@app_api.route('/<string:mod_name>/<string:control_name>/<string:method>/', methods=['GET', 'POST'])
def parse(mod_name, control_name, method):
    kwargs = request.form.to_dict()
    mod = None
    for element in dir(actioner):
        var = getattr(actioner, element)
        if issubclass(var, BaseActioner) and var.get_name() == mod_name:
            mod = var()
            break
    try:
        resp = mod.run_action(control_name, method, kwargs)
    except RequestException as e:
        return str(e.kwargs['errmess']), e.kwargs['errcode']
    # if not mod.register_action(control_name, method, kwargs):
    #     return '', 400
    # resp = mod.run_control()
    return resp
