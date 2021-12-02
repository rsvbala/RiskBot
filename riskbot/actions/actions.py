# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


entity_mapping = {
    "exploits": "exploit",
    "exploit": "exploit",
    "ransomwares": "ransomware",
    "ransomware": "ransomware",
    "cves": "cve",
    "cve": "cve",
    "vulnerabilities": "cve",
    "vulnerability": "cve"
}

entity_to_id_mapping = {
    "cve": "id",
    "ransomware": "name",
    "exploit": "title"
}

class ActionSendCount(Action):

    def name(self) -> Text:
        return "action_send_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_entity = next(tracker.get_latest_entity_values("vuln"), None)
        if not current_entity:
            dispatcher.utter_message(
                text="Sorry I dont understand what you meant. I am still learning, please be more specific. Example : "
                     "How many ransomwares are in my system")
        else:
            response = requests.get("http://localhost:5000/{}/count".format(entity_mapping[current_entity.lower()]))
            if response.status_code == 200:
                response_json = response.json()
                dispatcher.utter_message(text="There are {} {}".format(response_json["c"], current_entity.lower()))

        return []


class ActionSendTrendCount(Action):

    def name(self) -> Text:
        return "action_send_trend_count"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_entity = next(tracker.get_latest_entity_values("vuln"), None)
        days = next(tracker.get_latest_entity_values("duration"), None)
        if not current_entity:
            dispatcher.utter_message(
                text="Sorry I dont understand what you meant. I am still learning, please be more specific. Example : "
                     "How many ransomwares are in my system")
        else:
            response = requests.get(
                "http://localhost:5000/{}/count?trending={}".format(entity_mapping[current_entity.lower()], days))
            if response.status_code == 200:
                response_json = response.json()
                dispatcher.utter_message(text="There are {} trending {}".format(response_json["c"], current_entity.lower()))

        return []


class ActionSendTrendData(Action):

    def name(self) -> Text:
        return "action_send_trend_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_entity = next(tracker.get_latest_entity_values("vuln"), None)
        days = next(tracker.get_latest_entity_values("duration"), None)
        if not current_entity:
            dispatcher.utter_message(
                text="Sorry I dont understand what you meant. I am still learning, please be more specific. Example : "
                     "How many ransomwares are in my system")
        else:
            response = requests.get(
                "http://localhost:5000/{}/data?trending={}".format(entity_mapping[current_entity.lower()], days))
            if response.status_code == 200:
                res_list = []
                response_json = response.json()
                for each in response_json:
                    res_list.append(each[entity_to_id_mapping[entity_mapping[current_entity.lower()]]])
                if res_list:
                    result = ", "
                    dispatcher.utter_message(
                        text="Trending {} are {}".format(current_entity.lower(), result.join(res_list)))
                else:
                    dispatcher.utter_message(text="No data found in the time frame")

        return []