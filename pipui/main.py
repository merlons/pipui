from typing import Dict, List, Any
from flask import Flask, request, jsonify, render_template
import pipui
from pipui.utils import get_installed_packages, uninstall_package, search_packages, install_package

app = Flask(__name__, template_folder=pipui.__path__[0] + "/templates")


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
    available_packages = search_packages(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return jsonify(results)


@app.route("/install/", methods=["GET"])
def read_install():
    q = request.args.get('q')
    version = request.args.get('version')
    mirror = request.args.get('mirror', "https://pypi.python.org/simple")

    try:
        install_package(f"{q}=={version}" if version else q, mirror)  # 假设这个函数会安装包
    except Exception as e:
        return {"msg": str(e)}

    return {"msg": "Install Successful!"}


@app.route("/interpreter-info", methods=["GET"])
def interpreter_info():
    import sys
    return {
        'version': sys.version,
        'path': sys.executable
    }


def main(host="0.0.0.0", port=6001):
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
