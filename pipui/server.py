import fire
from flask import Flask, request, jsonify, render_template
import pipui
from pipui.utils import PipManager, available_packages

app = Flask(__name__, template_folder=pipui.__path__[0] + "/templates")


@app.route("/interpreter-info", methods=["GET"])
def interpreter_info():
    pm = PipManager()
    return {'version': pm.version, 'path': pm.executable}


@app.route("/", methods=["GET"])
def read_root():
    return render_template("index.html")


@app.route("/installed", methods=["GET"])
def pip_list():
    packages = PipManager().pip_list()
    return jsonify(packages)


@app.route("/uninstall/<package_name>", methods=["DELETE"])
def pip_uninstall(package_name: str):
    success = PipManager().pip_uninstall(package_name)
    if not success:
        return jsonify({"detail": "Package not found"}), 404
    return jsonify({"message": f"Package {package_name} uninstalled successfully"})


@app.route("/search/", methods=["GET"])
def pip_search():
    q = request.args.get('q')
    # available_packages = PipManager().pip_search(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return jsonify(results)


@app.route('/install', methods=['POST'])
def pip_install():
    data = request.get_json()
    package_details = data.get('packageDetails')
    mirror_source = data.get('mirrorSource')

    # 在这里执行安装逻辑，比如调用系统命令安装包
    print(f"安装包：{package_details}，镜像源：{mirror_source}")
    try:
        PipManager().pip_install(package_details.replace('\n', ' ').replace("\r", ' '), mirror_source)  # 假设这个函数会安装包
    except Exception as e:
        return {"msg": str(e)}

    # 假设安装成功，返回成功响应
    return jsonify({"message": "安装成功"}), 200


def main(host="0.0.0.0", port=5000):
    app.run(host=host, port=port)



