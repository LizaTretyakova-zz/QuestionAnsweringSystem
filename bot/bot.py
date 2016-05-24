#!/usr/bin/env python3
from Bot import Bot

START = "start"
STOP = "stop"
RESTART = "restart"


def commit_action(action: str) -> int:
    try:
        commit_action.bot_daemon
    except AttributeError:
        commit_action.bot_daemon = Bot('/tmp/qa_bot.pid')

    if 'start' == action:
        commit_action.bot_daemon.start()
    elif 'stop' == action:
        commit_action.bot_daemon.stop()
    elif 'restart' == action:
        commit_action.bot_daemon.restart()
    else:
        print("Unknown command")
        return 2
    return 0
