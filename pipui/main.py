from typing import Dict, List, Any
from flask import Flask, request, jsonify, render_template
import pipui
from pipui.utils import get_installed_packages, uninstall_package, search_packages, install_package, available_packages

app = Flask(__name__, template_folder=pipui.__path__[0] + "/templates")


@app.route("/interpreter-info", methods=["GET"])
def interpreter_info():
    import sys
    version = sys.version_info
    return {
        'version': f"{version.major}.{version.minor}.{version.micro}",
        'path': sys.executable
    }


@app.route("/", methods=["GET"])
def read_root():
    packages = get_installed_packages()
    return render_template("index.html", packages=packages)


@app.route("/uninstall/<package_name>", methods=["DELETE"])
def delete_package(package_name: str):
    success = uninstall_package(package_name)
    if not success:
        return jsonify({"detail": "Package not found"}), 404
    return jsonify({"message": f"Package {package_name} uninstalled successfully"})


@app.route("/search/", methods=["GET"])
def search_package():
    q = request.args.get('q')
    # available_packages = search_packages(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return jsonify(results)


@app.route('/install', methods=['POST'])
def install():
    data = request.get_json()
    package_details = data.get('packageDetails')
    mirror_source = data.get('mirrorSource')

    # 在这里执行安装逻辑，比如调用系统命令安装包
    print(f"安装包：{package_details}，镜像源：{mirror_source}")
    try:
        install_package(package_details.replace('\n', ' ').replace("\r", ' '), mirror_source)  # 假设这个函数会安装包
    except Exception as e:
        return {"msg": str(e)}

    # 假设安装成功，返回成功响应
    return jsonify({"message": "安装成功"}), 200


def main(host="0.0.0.0", port=6001):
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
