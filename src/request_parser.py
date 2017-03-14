from flask import Blueprint, request
from actioner import BaseActioner, RequestException
import actioner

app_api = Blueprint('api', __name__)


@app_api.route('/auth/', methods=['POST'])
def auth():
    # print(dir(request))
    header_params = request.headers
    mod_name = 'auth'
    mod = None
    for element in dir(actioner):
        var = getattr(actioner, element)
        if issubclass(var, BaseActioner) and var.get_name() == mod_name:
            mod = var()
            break
    try:
        mod.register_action(header_params)
        resp = mod.run_action()
    except RequestException as e:
        return str(e.kwargs['errmess']), e.kwargs['errcode']
    # if not mod.register_action(control_name, method, kwargs):
    #     return '', 400
    # resp = mod.run_control()
    return resp


@app_api.route('/<string:mod_name>/<string:control_name>/<string:method>/', methods=['POST'])
# @app_api.route('/<string:mod_name>/<string:control_name>/<string:method>/', methods=['GET', 'POST'])
def parse(mod_name, control_name, method):
    kwargs = request.values.to_dict()
    header_params = request.headers
    mod = None
    for element in dir(actioner):
        var = getattr(actioner, element)
        if issubclass(var, BaseActioner) and var.get_name() == mod_name:
            mod = var()
            break
    try:
        mod.register_action(control_name, method, kwargs, header_params)
        resp = mod.run_action()
    except RequestException as e:
        return str(e.kwargs['errmess']), e.kwargs['errcode']
    # if not mod.register_action(control_name, method, kwargs):
    #     return '', 400
    # resp = mod.run_control()
    return resp
