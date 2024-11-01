from typing import Dict, List, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pipui
from pipui.utils import get_installed_packages, uninstall_package, search_packages, install_package, available_packages

app = FastAPI()
templates = Jinja2Templates(directory=pipui.__path__[0] + "/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    packages = get_installed_packages()
    return templates.TemplateResponse("index.html", {"request": request, "packages": packages})


@app.delete("/uninstall/{package_name}")
async def delete_package(package_name: str):
    success = uninstall_package(package_name)
    if not success:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"message": f"Package {package_name} uninstalled successfully"}


@app.get("/search", response_model=List[Dict[str, Any]])
async def search_package(q: str):
    available_packages = search_packages(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return results


@app.get("/install")
async def read_install(request: Request, q: str = None, version: str = None,
                       mirror: str = "https://pypi.python.org/simple"):
    try:
        install_package(f"{q}=={version}" if version else q, mirror)  # 假设这个函数会安装包
    except Exception as e:
        return {"msg": str(e)}

    return {"msg": "Install Successful!"}


@app.get("/interpreter-info", response_model=Dict[str, str])
def interpreter_info():
    import sys
    return {
        'version': sys.version,
        'path': sys.executable
    }


def main(host="0.0.0.0", port=6001):
    uvicorn.run("pipui.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
