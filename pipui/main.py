import sys
from typing import Dict, List, Any

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
            name = pkg.find('span', class_='package-snippet__name').text
            version_curr = pkg.find('span', class_='package-snippet__version').text
            description = pkg.find('p', class_='package-snippet__description').text.strip()

            response2 = requests.get(f'https://pypi.org/project/{name}/#history')
            if response2.status_code == 200:
                soup2 = BeautifulSoup(response2.text, 'html.parser')
                versions = [i.text.replace('\n', '').strip() for i in soup2.find_all('p', class_="release__version")]
            else:
                versions = [version_curr]
            pkg_info = {
                'name': name,
                'version': version_curr,
                'versions': versions,
                'description': description
            }
            results.append(pkg_info)
        return results

    return []


@app.get("/search", response_model=List[Dict[str, Any]])
async def search_package(q: str):
    # available_packages = search_packages(q)  # 替换为你的逻辑
    available_packages = [{'name': 'fire', 'version': '0.7.0', 'versions': ['0.7.0', '0.6.0', '0.5.0', '0.4.0', '0.3.1', '0.3.0', '0.2.1', '0.2.0', '0.1.3', '0.1.2', '0.1.1', '0.1.0'], 'description': 'A library for automatically generating command line interfaces.'}, {'name': 'python-fire', 'version': '0.1.0', 'versions': ['0.1.0'], 'description': 'FIRE HOT. TREE PRETTY'}, {'name': 'classy-fire', 'version': '0.2.1', 'versions': ['0.2.1', '0.1.9', '0.1.7', '0.1.6', '0.1.5', '0.1.4', '0.1.3', '0.1.1', '0.1.0'], 'description': 'Classy-fire is multiclass text classification approach leveraging OpenAI LLM model APIs optimally using clever parameter tuning and prompting.'}, {'name': 'forest-fire', 'version': '0.1.1', 'versions': ['0.1.1', '0.1'], 'description': 'Algerian Forest Fire Prediction Model'}, {'name': 'django-fire', 'version': '1.0.0', 'versions': ['1.0.0'], 'description': 'vulnerable password cleanser for django'}, {'name': 'dyneusr-fire', 'version': '0.0.3', 'versions': ['0.0.3', '0.0.1'], 'description': 'A command line interface for DyNeuSR'}, {'name': 'sanic-fire', 'version': '0.1', 'versions': ['0.1'], 'description': 'sanic-fire is an extension for Sanic that adds support for commands to your application.'}, {'name': 'dragons-fire', 'version': '0.2.0', 'versions': ['0.2.0', '0.1.9', '0.1.8', '0.1.6', '0.1.5'], 'description': 'A test suite to provide simple testing of workflows'}, {'name': 'fire-chat', 'version': '0.0.6', 'versions': ['0.0.6', '0.0.6.dev803345                  pre-release', '0.0.6.dev778541                  pre-release', '0.0.6.dev396970                  pre-release', '0.0.6.dev14228                  pre-release', '0.0.5', '0.0.4', '0.0.4.dev0                  pre-release', '0.0.3                  yanked', '0.0.3.dev0                  pre-release', '0.0.2                  yanked', '0.0.1                  yanked'], 'description': 'A CLI tool to chat with LLM models including GPT and Claude.'}, {'name': 'fire-detection', 'version': '0.0.1', 'versions': ['0.0.1'], 'description': 'A fire detecting library'}, {'name': 'fire-downloader', 'version': '1.0.3', 'versions': ['1.0.3', '1.0.2', '1.0.1', '1.0.0'], 'description': 'Package for downloading urls'}, {'name': 'fire-opal', 'version': '8.2.0', 'versions': ['8.2.0', '8.1.2', '8.1.1', '8.1.0', '8.0.0', '7.3.1', '7.3.0', '7.2.0', '7.1.0', '7.0.0', '6.9.0', '6.8.0', '6.7.0', '6.6.0', '6.5.0', '6.4.1', '6.4.0', '6.3.0', '6.2.1', '6.2.0', '6.1.1', '6.1.0', '6.0.1', '6.0.0', '5.3.2', '5.3.1', '5.3.0', '5.2.2', '5.2.1', '5.2.0', '5.1.1', '5.1.0', '5.0.0', '4.0.1', '4.0.0', '3.4.1', '3.4.0', '3.3.0', '3.2.0', '3.1.0', '3.0.0', '2.1.0', '2.0.1', '2.0.0', '1.0.0'], 'description': 'Fire Opal Client'}, {'name': 'fire-python', 'version': '0.42', 'versions': ['0.42', '0.41', '0.40', '0.34', '0.32', '0.31', '0.30', '0.29', '0.28', '0.27', '0.26', '0.25', '0.24', '0.23', '0.22', '0.21', '0.2'], 'description': 'Functional Inference and Reasoning Engine - Python'}, {'name': 'fire-split', 'version': '0.1.9', 'versions': ['0.1.9', '0.1.8', '0.1.7', '0.1.6', '0.1.5', '0.1.4', '0.1.3', '0.0.4', '0.0.3', '0.0.2'], 'description': 'Split individual fire events from tif files'}, {'name': 'fire-state', 'version': '0.1.3', 'versions': ['0.1.3', '0.1.2', '0.1.1', '0.1.0'], 'description': 'Persist state across multiple pages in streamlit.'}, {'name': 'pibooth-fire-remote', 'version': '0.2.2', 'versions': ['0.2.2', '0.2.0', '0.1.8', '0.1.7', '0.1.6', '0.1.5', '0.1.4', '0.1.3', '0.1.2'], 'description': ''}, {'name': 'forest-fire-clustering', 'version': '0.0.25', 'versions': ['0.0.25', '0.0.24', '0.0.21', '0.0.20', '0.0.19', '0.0.18', '0.0.17', '0.0.16', '0.0.15', '0.0.14', '0.0.13', '0.0.12', '0.0.11', '0.0.10', '0.0.9', '0.0.8', '0.0.7', '0.0.6', '0.0.5', '0.0.4', '0.0.3', '0.0.2'], 'description': 'Clustering method based on Forest Fire Dynamics'}, {'name': 'jenkins-fire-cli', 'version': '0.1.1', 'versions': ['0.1.1'], 'description': ''}, {'name': 'haas-python-fire', 'version': '0.0.8', 'versions': ['0.0.8', '0.0.7', '0.0.6', '0.0.5', '0.0.4', '0.0.3', '0.0.2', '0.0.1'], 'description': 'This is fire driver for HaaS Python. HaaS Python is forked from micropython.'}, {'name': 'nonebot-plugin-fire', 'version': '1.0.3', 'versions': ['1.0.3', '1.0.2', '1.0.1', '1.0.0'], 'description': 'nonebot2 plugin fire'}]

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
