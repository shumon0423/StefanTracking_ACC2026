import yaml
from pathlib import Path


def load_parameters(filename=None):
    if filename is None:
        filename = Path(__file__).parent.parent / "config" / "parameters.yaml"
    with open(filename, "r") as file:
        data = yaml.safe_load(file)
    p = data["physical"]
    p["alp"] = p["kc"] / p["rho"] / p["cp"]
    p["beta"] = p["kc"] / p["rho"] / p["Hf"]
    return data


params = load_parameters()
