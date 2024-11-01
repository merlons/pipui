import sys
from bs4 import BeautifulSoup
import subprocess
import requests


def get_installed_packages():
    try:
        packages = subprocess.check_output([sys.executable, "-m", 'pip', 'list', '--format=freeze'],
                                           stderr=subprocess.STDOUT, ).decode().replace('\r\n', '\n').split('\n')
        return [{'name': p.split('==')[0], 'version': p.split('==')[1]} for p in packages if '==' in p]
    except subprocess.CalledProcessError:
        return []


def uninstall_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name, index_url=None):
    if index_url:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--index-url", index_url])
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def get_available_versions(package_name):
    try:

        # 调用 pip index versions 命令并捕获输出
        result = subprocess.check_output(
            [sys.executable, "-m", 'pip', 'index', 'versions', package_name],
            stderr=subprocess.STDOUT,  # 将标准错误合并到标准输出
            # text=True  # 以文本模式返回输出
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.strip()}")
        return []

    # 解析输出
    versions = []
    for line in result.splitlines():
        line = line.decode()
        if "Available versions:" in line:
            versions = line.replace("Available versions:", "").replace(' ', '').split(',')
            break  # 找到后就退出循环

    return versions


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
            pkg_info = {
                'name': name,
                'version': version_curr,
                'versions': get_available_versions(name),
                'description': description
            }
            results.append(pkg_info)
        return results

    return []


available_packages = [
    {'name': 'fire', 'version': '0.7.0',
     'versions': ['0.7.0', '0.6.0', '0.5.0', '0.4.0', '0.3.1', '0.3.0', '0.2.1', '0.2.0', '0.1.3', '0.1.2', '0.1.1',
                  '0.1.0'],
     'description': 'A library for automatically generating command line interfaces.'},
    {'name': 'python-fire', 'version': '0.1.0', 'versions': ['0.1.0'],
     'description': 'FIRE HOT. TREE PRETTY'},
    {'name': 'classy-fire', 'version': '0.2.1',
     'versions': ['0.2.1', '0.1.9', '0.1.7', '0.1.6', '0.1.5', '0.1.4', '0.1.3', '0.1.1', '0.1.0'],
     'description': 'Classy-fire is multiclass text classification approach leveraging OpenAI LLM model APIs optimally using clever parameter tuning and prompting.'},
    {'name': 'forest-fire', 'version': '0.1.1', 'versions': ['0.1.1', '0.1'],
     'description': 'Algerian Forest Fire Prediction Model'},
    {'name': 'django-fire', 'version': '1.0.0', 'versions': ['1.0.0'],
     'description': 'vulnerable password cleanser for django'},
]
