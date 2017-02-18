from flask import Blueprint, request
from actioner import BaseActioner, RequestException
import actioner

app_api = Blueprint('api', __name__)

@app_api.route('/<string:mod_name>/<string:control_name>/<string:method>/')
def parse(mod_name, control_name, method):
    kwargs = request.args.to_dict()
    mod = None
    for element in dir(actioner):
        var = getattr(actioner, element)
        if issubclass(var, BaseActioner) and var.get_name() == mod_name:
            mod = var()
            break
    try:
        mod.register_action(control_name, method, kwargs)
        resp = mod.run_control()
    except RequestException as e:
        return str(e.args), 400
    # if not mod.register_action(control_name, method, kwargs):
    #     return '', 400
    # resp = mod.run_control()
    return resp
