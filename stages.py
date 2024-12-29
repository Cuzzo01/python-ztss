import random

from helpers.file_handlers import append_to_secrets
from helpers.general_helpers import (
    get_random_number,
    swap_ids,
    load_current_ids,
    load_previous_locations,
)
from models import Datafile, AppConfig


def perform_stage_zero(datafile: Datafile, config: AppConfig):
    print(f"Performing Stage 0 operation for {config.current_user}")
    receiving_id = get_random_number(datafile, config)
    giving_id = get_random_number(datafile, config)

    print(f"Adding new receiving ID: {receiving_id}")
    datafile.receiving_ids.append(receiving_id)
    print(f"Adding new giving ID: {giving_id}")
    datafile.giving_ids.append(giving_id)
    datafile.shuffle_ids()

    secrets_entry = {
        f"stage0-{config.current_user}": {"ids": [receiving_id, giving_id]}
    }
    append_to_secrets(secrets_entry, config)


def perform_stage_one(datafile: Datafile, config: AppConfig):
    print(f"Performing Stage 1 operation for {config.current_user}")
    turn_number = config.order.index(config.current_user)
    last_turn_number = len(config.order) - 1

    did_shunt = False
    if turn_number == 0:
        print("You're the first person in the order, we need to shuffle and shunt.")
        datafile.shuffle_ids()
        datafile.shunt_ids()
        did_shunt = True
    elif turn_number != last_turn_number:
        should_shunt = random.random() > 0.5
        if should_shunt:
            print("Coin flip came up heads, we'll do a shunt.")
            datafile.shunt_ids()
            did_shunt = True
        else:
            print("Coin flip came up tails, skipping the shunt.")
    else:
        print("You're the last person, no shunting allowed.")

    last_ids = load_current_ids(last_stage_num=0, config=config)
    new_ids, swapped_id_pairs = swap_ids(datafile, last_ids, config)
    secrets_entry = {
        f"stage1-{config.current_user}": {
            "ids": new_ids,
            "did_shunt": did_shunt,
            "swapped_ids": swapped_id_pairs,
        }
    }
    append_to_secrets(secrets_entry, config)


def perform_stage_two(datafile: Datafile, config: AppConfig):
    print(f"Performing Stage 2 operation for {config.current_user}")
    last_ids = load_current_ids(1, config)

    current_receiving_index = datafile.receiving_ids.index(last_ids[0])
    print(f"Your receiving index is {current_receiving_index}!")
    current_giving_index = datafile.giving_ids.index(last_ids[1])
    print(f"Your receiving index is {current_giving_index}!")
    print(
        "These values shouldn't change from now on, saving them to secrets file for later checking."
    )

    new_ids, swapped_id_pairs = swap_ids(datafile, last_ids, config)
    secrets_entry = {
        f"stage2-{config.current_user}": {
            "ids": new_ids,
            "swapped_ids": swapped_id_pairs,
            "locations": {
                "receiving": current_receiving_index,
                "giving": current_giving_index,
            },
        }
    }
    append_to_secrets(secrets_entry, config)


def perform_stage_three(datafile: Datafile, config: AppConfig):
    print(f"Performing Stage 3 operation for {config.current_user}")
    last_ids = load_current_ids(2, config)
    previous_locations = load_previous_locations(config)

    datafile.verify_id_locations(last_ids, previous_locations)

    new_ids, swapped_id_pairs = swap_ids(datafile, [last_ids[1]], config)
    datafile.swap_ids(last_ids[0], config.current_user)
    swapped_id_pairs.append(f"From {last_ids[0]} to {config.current_user}")

    secrets_entry = {
        f"stage3-{config.current_user}": {
            "ids": new_ids,
            "swapped_ids": swapped_id_pairs,
        }
    }
    append_to_secrets(secrets_entry, config)


def perform_stage_four(datafile: Datafile, config: AppConfig):
    print(
        f"Performing Stage 4 operation for {config.current_user}. Let's find out who you got."
    )

    last_ids = load_current_ids(last_stage_num=3, config=config)
    previous_locations = load_previous_locations(config)

    datafile.verify_id_locations([config.current_user, last_ids[0]], previous_locations)

    giving_index = datafile.giving_ids.index(last_ids[0])
    print(f"Your giving index is {giving_index}.")
    receiving_id = datafile.receiving_ids[giving_index]
    print(f"\n\nThis means you're giving to {receiving_id}!\n\n")

    new_ids, swapped_id_pairs = swap_ids(datafile, last_ids, config)
    secrets_entry = {
        f"stage4-{config.current_user}": {
            "ids": new_ids,
            "gifting_to": receiving_id,
            "swapped_ids": swapped_id_pairs,
        }
    }
    append_to_secrets(secrets_entry, config)
    pass


stage_dict = {
    0: perform_stage_zero,
    1: perform_stage_one,
    2: perform_stage_two,
    3: perform_stage_three,
    4: perform_stage_four,
}
