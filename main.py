import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import subprocess
import pkg_resources

def get_installed_packages():
    try:
        result = subprocess.run(['pip', 'list', '--format=freeze'], capture_output=True, text=True, check=True)
        packages = result.stdout.strip().split('\n')
        return [{'name': p.split('==')[0], 'version': p.split('==')[1]} for p in packages if '==' in p]
    except subprocess.CalledProcessError:
        return []

def uninstall_package(package_name):
    try:
        subprocess.check_call(["pip", "uninstall", "-y", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
