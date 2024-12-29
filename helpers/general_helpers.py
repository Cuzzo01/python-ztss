from typing import Tuple, Optional
from pathlib import Path
import random

from models import AppConfig, Datafile
from helpers.file_handlers import load_raw_yaml


def get_random_number(datafile: Datafile, config: AppConfig) -> str:
    upper_bound = config.max_random_number - 1
    max_number_digits = len(str(upper_bound))

    while True:
        if config.prompt_user_for_random_numbers:
            rand_num = get_number_from_user(upper_bound)
        else:
            rand_num = random.randint(0, upper_bound)

        rand_num = str(rand_num).zfill(max_number_digits)
        if datafile.id_is_free(rand_num):
            print(f"Generated new ID: {rand_num}")
            break
        else:
            print(f"Oops, ID '{rand_num}' is already being used. Let's get another.")

    return str(rand_num).zfill(max_number_digits)


def get_number_from_user(upper_bound: int):
    while True:
        try:
            user_input = input(
                f"Time to pick a number! (between 0 and {upper_bound} please): "
            )
            number = int(user_input)

            if 0 <= number <= upper_bound:
                return number
            else:
                print(f"Error: Number must be between 0 and {upper_bound}")

        except ValueError:
            print("Error: Please enter a valid number")


def swap_ids(datafile: Datafile, old_ids: list[str], config: AppConfig) -> list[str]:
    new_ids = [get_random_number(datafile, config) for _ in range(len(old_ids))]
    swapped_ids = list(zip(old_ids, new_ids))

    for old_value, new_value in swapped_ids:
        datafile.swap_ids(old_value, new_value)

    swapped_ids_str = [f"From {old} to {new}" for old, new in swapped_ids]
    return new_ids, swapped_ids_str


def load_current_ids(last_stage_num: int, config: AppConfig):
    print(f"Loading IDs for {config.current_user} from Stage {last_stage_num}.")
    secrets_yaml = load_raw_yaml(config.secrets_path)
    previous_secrets = secrets_yaml[f"stage{last_stage_num}-{config.current_user}"]
    if previous_secrets is None:
        print("\nMissing secrets from previous stage! Can't continue.")
        return

    previous_ids = previous_secrets["ids"]
    print(f"Previous IDs are {previous_ids}")
    return previous_ids


def load_previous_locations(config: AppConfig):
    stage_number = 2  # Locations are captured on Stage 2 and don't change
    print(
        f"Loading previously seen locations for {config.current_user} from Stage {stage_number}."
    )
    secrets_yaml = load_raw_yaml(config.secrets_path)
    previous_secrets = secrets_yaml[f"stage{stage_number}-{config.current_user}"]
    if previous_secrets is None:
        print("\nMissing secrets from previous stage! Can't continue.")
        raise f"Missing expected secrets for {config.current_user} in Stage {stage_number}"

    previous_locations = previous_secrets["locations"]
    print(f"Previous locations were {previous_locations}")
    return [previous_locations["receiving"], previous_locations["giving"]]


def is_current_users_turn(last_user_turn_num: str, config: AppConfig):
    current_user = config.current_user
    current_user_turn_num = config.order.index(current_user)
    if last_user_turn_num is None:
        last_user_turn_num = -1

    user_to_go = last_user_turn_num + 1
    if user_to_go == len(config.order):
        user_to_go = 0

    is_turn = user_to_go == current_user_turn_num
    if not is_turn:
        print(
            f"\nIt's not your turn, check that the latest datafile is in output directory.\nCurrent user is {current_user} but it's {config.order[user_to_go]}'s turn."
        )

    return is_turn


def find_latest_datafile_path(
    config: AppConfig,
) -> Tuple[Optional[Path], Optional[int], Optional[int]]:
    # Get all files that match the pattern
    files = [
        f
        for f in Path(config.output_directory).iterdir()
        if f.is_file() and config.datafile_pattern_regex.match(f.name)
    ]

    # If no files match the pattern, return None
    if not files:
        return None, None, None

    # Sort the files by stage and user number (both are integers)
    def get_stage_user_numbers(file: Path):
        match = config.datafile_pattern_regex.match(file.name)
        stage, user = map(int, match.groups())
        return stage, user

    # Find the file with the largest stage and user numbers
    latest_file = max(files, key=get_stage_user_numbers)

    stage, user = get_stage_user_numbers(latest_file)
    return latest_file, stage, user
