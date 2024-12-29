import yaml
from pathlib import Path

from models import AppConfig, Datafile


def load_config(path: str) -> AppConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)


def load_datafile(path: Path) -> Datafile:
    with path.open("r") as f:
        data = yaml.safe_load(f)
    return Datafile(**data)


def save_datafile(stage: int, file: Datafile, config: AppConfig):
    data_dict = file.to_yaml_dict()

    current_user_turn_num = str(config.order.index(config.current_user))
    datafile_template = config.datafile_pattern

    file_name = datafile_template.replace("{Stage}", str(stage)).replace(
        "{UserNum}", current_user_turn_num
    )
    file_path = f"{config.output_directory}/{file_name}"
    print(f"\nSaving output file to:\t{file_path}")
    with open(file_path, "w") as f:
        yaml.dump(data_dict, f, default_flow_style=False)


def append_to_secrets(entry: dict, config: AppConfig):
    print("Writing to secrets file.")
    append_to_yaml(config.secrets_path, entry)


def append_to_yaml(file_path: str, data: dict):
    with open(file_path, "a") as f:
        yaml.dump(data, f, default_flow_style=False)


def load_raw_yaml(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
