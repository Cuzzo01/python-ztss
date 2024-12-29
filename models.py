from pydantic import BaseModel, model_validator
from typing import List
import re
import random


class AppConfig(BaseModel):
    order: List[str]
    current_user: str
    max_random_number: int
    secrets_path: str
    output_directory: str
    datafile_pattern: str
    datafile_pattern_regex: re.Pattern[str]
    prompt_user_for_random_numbers: bool

    @model_validator(mode="before")
    def parse_pairs(cls, values) -> dict:
        pattern = values.get("datafile_pattern", "")
        values["datafile_pattern_regex"] = re.compile(
            pattern.replace("{Stage}", r"(\d+)").replace("{UserNum}", r"(\d+)")
        )
        return values


class Datafile(BaseModel):
    receiving_ids: List[str] = []
    giving_ids: List[str] = []

    def id_is_free(self, id: str):
        return id not in self.receiving_ids and id not in self.giving_ids

    def verify_id_locations(self, ids: list[str], previous_locations: list[str]):
        try:
            current_receiving_location = self.receiving_ids.index(ids[0])
            if current_receiving_location is not previous_locations[0]:
                print(
                    "\n\n!!! Your receiving ID has moved, something may be afoot. !!!\n\n"
                )
            else:
                print(f"Receiving ID still in the expected location")

            current_giving_location = self.giving_ids.index(ids[1])
            if current_giving_location is not previous_locations[1]:
                print(
                    "\n\n!!! Your giving ID has moved, something may be afoot. !!!\n\n"
                )
            else:
                print(f"Giving ID still in the expected location.")
        except:
            print(
                "\n\n!!! Encountered an error trying to validate ID locations, something may be afoot. !!!\n\n"
            )

    def swap_ids(self, old_value: str, new_value: str):
        """
        This method swaps the old_value with new_value in both receiving_ids and giving_ids lists.
        """
        print(f"Swapping ID from {old_value} to {new_value}")
        # Search and replace in receiving_ids
        for i in range(len(self.receiving_ids)):
            if self.receiving_ids[i] == old_value:
                self.receiving_ids[i] = new_value

        # Search and replace in giving_ids
        for i in range(len(self.giving_ids)):
            if self.giving_ids[i] == old_value:
                self.giving_ids[i] = new_value

    # Method to shuffle both lists in the same way
    def shuffle_ids(self):
        print("Performing a shuffle.")
        # Pair up the receiving_ids and giving_ids
        paired = list(zip(self.receiving_ids, self.giving_ids))

        # Shuffle the paired list
        random.shuffle(paired)

        # Unpack the pairs back into the original lists
        self.receiving_ids, self.giving_ids = zip(*paired)

        # Convert back from tuple to list
        self.receiving_ids = list(self.receiving_ids)
        self.giving_ids = list(self.giving_ids)

    def shunt_ids(self):
        print("Performing a shunt.")
        # Ensure the list is not empty
        if self.giving_ids:
            # Shunt the giving_ids over by 1 (wrap the last element to the first position)
            self.giving_ids = [self.giving_ids[-1]] + self.giving_ids[:-1]

    # Extract receivingIds and givingIds from pairs before validation
    @model_validator(mode="before")
    def parse_pairs(cls, values) -> dict:
        pairs = values.get("pairs", [])
        receiving_ids = []
        giving_ids = []

        # Split each pair into receivingIds and givingIds
        for pair in pairs:
            try:
                first, second = pair.split(",")
                receiving_ids.append(first)
                giving_ids.append(second)
            except ValueError:
                raise ValueError(f"Invalid pair format: {pair}")

        # Set the values for receivingIds and givingIds
        values["receiving_ids"] = receiving_ids
        values["giving_ids"] = giving_ids
        return values

    # Convert data to dictionary with only pairs as strings
    def to_yaml_dict(self):
        pairs = [f"{r},{g}" for r, g in zip(self.receiving_ids, self.giving_ids)]

        return {"pairs": pairs}
