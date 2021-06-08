import pandas as pd

import logging
import http.server
import requests
import os
import re

import config


def main():
    # url = "https://www.warcraftlogs.com:443/v1/report/events/damage-taken/tTyCz1adrZqQN67c?end=50000000&api_key=60b7fc2230974cb91173cd1e585f3e85"
    # response = requests.get(url)
    # response = response.json()
    # df = pd.DataFrame(response['events'])
    logging.basicConfig(handlers=[logging.StreamHandler()])

    logging.info("Starting")

    player_id_regex = re.compile(r"Player-[0-9]{2}-[0-9A-Z]{8}")
    player_name_regex = re.compile("(?<=Player-[0-9]{2}-[0-9A-Z]{8},\")\\D*(?=\")")

    file = os.path.abspath(r"C:\Program Files (x86)\World of Warcraft\_retail_\Logs\WoWCombatLog-052621_210739.txt")

    # log_data = [line.replace("  ", ",").replace("\n", "") for line in open(file, mode='r')]
    log_data = [line.replace("\n", "") for line in open(file, mode='r')]

    # df = pd.read_csv(log_data)
    df = pd.DataFrame(columns=['timestamp', 'encounter', 'character', 'action', 'amount'])

    encounter_code = None
    for line in log_data:
        try:
            timestamp = re.search("^.*(?<=\\s\\s)", line).group().strip()
        except AttributeError:
            continue

        encounter_code = ""
        encounter_name = ""
        if 'ENCOUNTER_START' in line:
            encounter_code = re.search("[0-9]{4}", line).group()
            encounter_name = re.search("(?<=[0-9]{4},\")\\D*(?=\",)", line).group()
        elif 'ENCOUNTER_END' in line:
            encounter_code = ""
            encounter_name = ""

        player_dict = {}
        player_name = None
        if 'COMBATANT_INFO' not in line:
            player_id = player_id_regex.search(line)
            if player_id:
                player_id = player_id.group()
                player_name = player_dict.get(player_id, False)

                if not player_name:
                    try:
                        player_name = player_name_regex.search(line).group()
                        player_dict.update({player_id: player_name})
                    except AttributeError:
                        player_name = ""

        # Write to DF
        temp_df = pd.DataFrame(data={'timestamp': timestamp,
                                     'encounter': encounter_name,
                                     'character': player_name}, columns=['timestamp', 'encounter', 'character'])

        df.append(temp_df, ignore_index=True)
        # print("pause")

    print("pause")


def _get_logs_json(url: str) -> dict:
    pass


if __name__ == "__main__":
    main()
