import logging
import subprocess

import fire
from flask import Flask, request, jsonify, render_template
# from flask_wtf.csrf import CSRFProtect
import pipui
from pipui.utils import PipManager, available_packages

app = Flask(__name__, template_folder=pipui.__path__[0] + "/templates")
app.config['SECRET_KEY'] = 'your-secret-key'  # 设置一个强密钥
# csrf = CSRFProtect(app)
logging.basicConfig(level=logging.INFO)

pm = PipManager()


def make_response(data, code, msg):
    return jsonify(data=data, code=code, msg=msg)


@app.route("/", methods=["GET"])
def read_root():
    return render_template("index.html")


@app.route("/interpreter-info", methods=["GET"])
def interpreter_info():
    return make_response(data={'version': pm.version, 'path': pm.executable}, code=200, msg="Success")


@app.route("/installed", methods=["GET"])
def pip_list():
    packages = pm.pip_list()
    return make_response(data=packages, code=200, msg="Success")


@app.route("/uninstall/<package_name>", methods=["DELETE"])
def pip_uninstall(package_name: str):
    success = pm.pip_uninstall(package_name)
    if not success:
        return make_response(data={}, code=404, msg="Package not found")
    return make_response(data={"message": f"Package {package_name} uninstalled successfully"}, code=200, msg="Success")


@app.route("/search/", methods=["GET"])
def pip_search():
    q = request.args.get('q', '')
    available_packages = PipManager().pip_search(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return make_response(data=results, code=200, msg="Success")


@app.route('/install', methods=['POST'])
def pip_install():
    data = request.get_json()
    package_details = data.get('packageDetails', '')
    mirror_source = data.get('mirrorSource', '')

    errors = pm.pip_install(package_details.replace('\n', ' ').replace("\r", ' '), mirror_source)
    if errors:
        logging.info(f"安装包：{package_details}，镜像源：{mirror_source} 成功")
        return make_response(data={"msg": str(errors)}, code=500, msg=str(errors))

    return make_response(data={"message": "安装成功"}, code=200, msg="Success")


def main(host="0.0.0.0", port=5000):
    app.run(host=host, port=port)
