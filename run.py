from flask import Flask
from dashboards.seva import SevaDash
assets_dir = "assets"


def run():
    server = Flask(__name__)
    dashboard = SevaDash(__name__,server)
    dashboard.run()

if __name__ == "__main__":
    run()