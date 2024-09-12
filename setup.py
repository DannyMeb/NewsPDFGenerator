from setuptools import setup, find_packages
import subprocess
import sys

def install_packages():
    requirements = [
        'newsapi-python',
        'requests',
        'beautifulsoup4',
        'reportlab',
        'PyPDF2'
    ]
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    install_packages()

if __name__ == "__main__":
    main()
