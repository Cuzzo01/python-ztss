from helpers.file_handlers import load_config, load_datafile, save_datafile
from helpers.general_helpers import find_latest_datafile_path, is_current_users_turn
from stages import stage_dict
from models import Datafile


def main():
    config = load_config("config.yaml")
    try:
        current_user_turn_num = config.order.index(config.current_user)
        print(
            f"Current user is: {config.current_user} (turn number {current_user_turn_num})"
        )
    except:
        print("\nCurrent user does not appear in Order list.")
        return

    most_recent_datafile_path, stage, last_user_turn_num = find_latest_datafile_path(
        config
    )
    if most_recent_datafile_path is not None:
        print("Most recent datafile is:", most_recent_datafile_path)
        datafile = load_datafile(most_recent_datafile_path)
    else:
        print("No datafile found, generating a new one.")
        datafile = Datafile()

    if not is_current_users_turn(last_user_turn_num, config):
        return

    if stage is None:
        print("Assuming this is the first stage since we didn't have a datafile.")
        stage = 0
    elif current_user_turn_num == 0:
        stage += 1
        print(f"You're the first person in the cycle, first round of stage {stage}!")

    stage_action = stage_dict.get(stage)
    if stage_action is None:
        raise ValueError(f"Have no action for Stage {stage}")

    stage_action(datafile, config)

    save_datafile(stage, datafile, config)

    next_user_index = current_user_turn_num + 1
    next_user_index = next_user_index % len(config.order)
    next_user_name = config.order[next_user_index]

    if stage == 4 and next_user_index == 0:
        print(
            "\nYou're the last one in the list. Everyone should know who they're gifting to!"
        )
    else:
        print(f"Next user in the order is {next_user_name}. Send them the above file.")


main()
