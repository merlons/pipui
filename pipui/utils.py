import sys
from bs4 import BeautifulSoup
import subprocess
import requests


def subprocess_run(cmd):
    result = subprocess.run(
        cmd,
        check=False,  # 如果命令返回非零退出码，将引发 CalledProcessError
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获标准错误输出
        universal_newlines=True  # 转换输出为文本字符串（在 Python 3.6 中替代 text=True）
    )
    return result


class PipManager:
    def __init__(self):
        self.executable = sys.executable  # 解释器路径
        version = sys.version_info
        self.version = f"{version.major}.{version.minor}.{version.micro}"

    def pip_list(self):
        result = subprocess_run([self.executable, "-m", 'pip', 'list', '--format=freeze'])
        if result.returncode != 0:
            print(result.stderr)
            return []
        packages = result.stdout.replace('\r\n', '\n').split('\n')
        return [{'name': p.split('==')[0], 'version': p.split('==')[1]} for p in packages if '==' in p]

    def pip_uninstall(self, package_name):
        subprocess_run([self.executable, "-m", "pip", "uninstall", "-y", package_name])

    def pip_install(self, package_name, index_url=None):
        errors = []
        for i in package_name.split(' '):
            if not i:
                continue
            i = i.split("#")[0]
            if index_url:
                result = subprocess_run([self.executable, "-m", "pip", "install", i, "--index-url", index_url])
                if result.returncode != 0:
                    print(result.stderr)
                    errors.append(result.stderr)

            else:
                result = subprocess_run([self.executable, "-m", "pip", "install", i])
                if result.returncode != 0:
                    print(result.stderr)
                    errors.append(result.stderr)
        return errors

    def pip_search_versions(self, package_name):
        result = subprocess_run([self.executable, "-m", 'pip', 'index', 'versions', package_name])
        if result.returncode != 0:
            print(result.stderr)
            return []

        # 解析输出
        versions = []
        for line in result.stdout.replace('\r\n', '\n').split('\n'):
            if "Available versions:" in line:
                versions = line.replace("Available versions:", "").replace(' ', '').split(',')
                break  # 找到后就退出循环

        return versions

    def pip_search(self, query="a"):
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
                    'versions': self.pip_search_versions(name),
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
