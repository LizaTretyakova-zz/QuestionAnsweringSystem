import sys
import tests
import src
import bot
from psycopg2 import Error as Psycopg2Error
from psycopg2 import Warning as Psycopg2Warning
import config

logger = config.get_logger()


def main(argv=None):
    args = argv
    if args is None:
        args = sys.argv
    try:
        if args[1] == "test":
            tests.run_tests()
        elif args[1] == "ask":
            src.run(args[2])
        elif args[1] == "bot":
            bot.run_bot()
        else:
            print("Unknown command line argument")
            logger.error("Unknown command line argument %s", args[1])
            return 1
    except IndexError as err:
        logger.exception(err)
        print("Not enough arguments")
        return 1
    except KeyError as err:
        logger.exception(err)
        print("Possible problems with JSON config. Please see logs for more information")
        return 1
    except Psycopg2Error as err:
        logger.exception(err)
        print("Problems with database. Please, check its existence and correctness of your login and password.")
        return 1
    except Psycopg2Warning as err:
        logger.exception(err)
        print("Sorry, we're experiencing problems with database.")
        return 1
    except Exception as err:
        logger.exception(err)
        print("An unexpected error occurred. For more information see the log file.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())