import requests

bot_key = "6102348896:AAFwFZ17mggFwdCTlEB9K9fKLilAoaqx-5g"
channel = "@GeoGisBot_test"


def bot_notification(user, name, geom, description):
    geom = geom.split("(")[1][:-1]

    requests.get(
        f"https://api.telegram.org/bot{bot_key}/sendMessage",
        {
            "chat_id": channel,
            "text": f"User: {user} \n"
            f"Location: {name}\n"
            f"{description}\n"
            f"Coordinates: {geom}",
        },
    )
