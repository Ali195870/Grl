from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
import os 

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Alive"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=5000)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()


class RunBot:
    room_id = os.environ['Room_id']
    bot_token = os.environ['Token']
    bot_file = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id, self.bot_token)
        ]  # More BotDefinition classes can be added to the definitions list

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception as e:
                # Handle the exception
                print("Caught an exception:")
                print(e)
                time.sleep(1)
                continue


if __name__ == "__main__":
    web_server = WebServer()
    web_server.keep_alive()

    bot = RunBot()
    bot.run_loop()
