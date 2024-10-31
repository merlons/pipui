import sys
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import subprocess
import pkg_resources
from fastapi.responses import RedirectResponse
import requests


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


import pipui

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


def search_packages(query="a"):
    if query:
        response = requests.get(f'https://pypi.org/search/?q={query}')
    else:
        response = requests.get(f'https://pypi.org/search')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for pkg in soup.find_all('a', class_='package-snippet'):
            results.append({
                'name': pkg.find('span', class_='package-snippet__name').text,
                'version': pkg.find('span', class_='package-snippet__version').text,
                'description': pkg.find('p', class_='package-snippet__description').text.strip()
            })
        return [
            {
                'name': pkg.find('span', class_='package-snippet__name').text,
                'version': pkg.find('span', class_='package-snippet__version').text,
                'description': pkg.find('p', class_='package-snippet__description').text.strip()
            }
            for pkg in soup.find_all('a', class_='package-snippet')
        ]
    return []


@app.get("/search", response_model=List[Dict[str, str]])
async def search_package(q: str):
    available_packages = search_packages(q)  # 替换为你的逻辑
    results = [pkg for pkg in available_packages if q.lower() in pkg["name"].lower()]
    return results


def install_package(package_name, index_url=None):
    if index_url:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--index-url", index_url])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


@app.get("/install", response_class=HTMLResponse)
async def read_install(request: Request, q: str = None, mirror: str = "https://pypi.python.org/simple"):
    try:
        install_package(q, mirror)  # 假设这个函数会安装包
    except Exception as e:
        return f"<html><body><h1>Error: {str(e)}</h1></body></html>"

    return "<html><body><h1>Install Successful!</h1></body></html>"


@app.get("/interpreter-info", response_model=Dict[str, str])
def interpreter_info():
    import sys
    return {
        'version': sys.version,
        'path': sys.executable
    }


def main(host="0.0.0.0", port=8008):
    uvicorn.run("pipui.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
