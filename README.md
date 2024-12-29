# Zero Trust Secret Santa

A Python implementation of Matt Parker's "Zero Trust Secret Santa" procedure (from [this](https://www.youtube.com/watch?v=wqOb5n3BIn0) video). 

This script makes it possible to host a Zero Trust Secret Santa without having to explain the procedure to everyone in the group (though they will need basic familiarity with running a Python script). 

## Description 

A Zero Trust Secret Santa is a method of conducting a gift exchange where no single participant or central authority knows all the assignments. This ensures privacy, fairness, and decentralization while preventing malicious interference.

## Goals

From Matt Parker's description of the procedure (description of the video linked above):
- No central authority needed.  
- Can be done remotely with no hidden information.  
- Ensures participants do not get their own name.  
- Prevents malicious actors from exploiting the system without breaking it entirely.

## Usage

Each participant in the group must have a matching `order` list in their `config.yaml` file. The simplest approach is for one person to create a generic `config.yaml` file and share it with the group. Then, each participant updates the `current_user` line in the config with their own name.  

1. #### Get the Code

    Either clone the repo
    ```bash
    git clone [REPO URL]
    ```
    or get a ZIP from the person running your group.

0. #### Install Dependencies

    This script requires the `pyyaml` and `pydantic` Python packages. They can be installed with this command.
    ```
    pip install -r requirements.txt
    ```
    *If you're on macOS, you may need to replace `pip` with `pip3`.*

0. #### Update `config.yaml` (optional)

    If you received the `config.yaml` from someone else, you might need to update it. 
        
    - Open the `config.yaml` file and verify that the `current_user` line contains your name.
    - If it doesn’t, copy your name from the `order` list (ignore the `-` and copy only the name itself) and update the `current_user` line.

    It should look like this:

    ```yaml
    current_user: [YOUR NAME HERE]
    ```

0. #### Get Datafile (if you're not the first person)

    *If you're the first person in the order, you're good to skip to the next step.*

    If you're not, you'll need to wait to get a datafile from the person before you in the order. When you get it, take the file and save it into the `data` folder in the repo.

0. #### Run the Script
    
    Run the following command in a terminal (use `python3` on macOS if needed):
    ```bash
    python index.py
    ```

0. #### Check the Output

    If all goes well, you should see a message that looks like this
    ```
    Saving output file to:  ./data/[FILE_NAME].yaml
    Next user in the order is [USER_NAME]. Send them the above file.
    ```
    If you see something else, check the [troubleshooting](#troubleshooting) section below.

0. #### Share the File
    Now just send the file from in the message from the last step to who the script says.
    
    ##### Important:

    - Only send the file to the specified participant.
    - Avoid sharing files with the entire group, as this will compromise the secrecy of the procedure.

    Sharing via email or Discord DMs may be easiest. 

0. #### Repeat

    After 4 loops around the group, everyone should know who they're gifting to! If you missed the final message, check `data/secrets.yaml` for your assigned recipient.

## How It Works
*For a detailed breakdown of the procedure, see [PROCEDURE.md](PROCEDURE.md).*  

1. The script begins by reading the `config.yaml` file and locating the most recent datafile in the `data` directory.  
0. It determines:
   - The current stage of the procedure.  
   - Whose turn it is.  
0. It verifies the `current_user` in `config.yaml` matches the user who's turn it is.  
0. If it’s the correct user’s turn:
   - The appropriate operation, as defined in the procedure, is applied to the datafile.  
   - A new datafile is generated and saved in the `data` folder.  
0. The script outputs:  
   - The name of the new file.  
   - The next participant in the order (to whom the file should be sent).  
0. In stages 3 and 4, the script performs additional verification to ensure the user's position in the `order` list has not changed.

## Troubleshooting

#### `It's not your turn ...` Message

- If `it's [NAME]'s turn.` and [NAME] is the person before you:
    - You probably haven't saved the new datafile to the data directory. 
- If `it's [NAME]'s turn.` and [NAME] is the person after you:
    - You probably already ran the script. You just need to send the most recent datafile to the next person in the order.

#### `Current user does not appear in Order list.`

In the `config.yaml`, the `current_user` filed must match an entry in the `order` list ***exactly***. It's recommended you copy and paste a name off the order list and into the `current_user` field to make sure they match.

## Running a group
If you’re organizing the Secret Santa group:  

1. **Create the `config.yaml` File:**  
   - Add all participants’ names to the `order` list in the correct sequence.  

    Example `config.yaml`:
    ```yaml
    current_user: Alice
    prompt_user_for_random_numbers: false

    # Participants: Change with caution
    order: 
    - Alice
    - Bob
    - Eve
    - Malory
    - Trudy
    max_random_number: 10_000
    output_directory: './data'
    secrets_path: './data/secrets.yaml'
    datafile_pattern: 'ZTSS_Stage-{Stage}_User-{UserNum}.yaml'
    ```
    *See [config.yaml](config.yaml) for comments explaining each value.*
2. **Share the Config File:**  
   - Distribute the `config.yaml` file to everyone in the group.  
   - Remind participants to update the `current_user` field with their own name before running the script.

3. **Guide Participants:**  
   - Explain the steps for running the script and sharing the datafiles.  
   - Emphasize the importance of following the order and only sharing files with the specified participant.
