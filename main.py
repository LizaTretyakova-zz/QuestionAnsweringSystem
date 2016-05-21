import sys
import tests
import src
from psycopg2 import Error as Psycopg2Error
from psycopg2 import Warning as Psycopg2Warning


def main(argv=None):
    args = argv
    if args is None:
        args = sys.argv
    try:
        if args[1] == "test":
            tests.run_general()
        elif args[1] == "ask":
            src.run(args[2])
        else:
            print("Unknown command line argument")
            return 1
    except IndexError:
        print("Not enough arguments")
        return 1
    except KeyError:
        print("Possible problems with JSON config. Please see logs for more information")
        return 1
    except Psycopg2Error:
        print("Problems with database. Please, check its existence and correctness of your login and password.")
        return 1
    except Psycopg2Warning:
        print("Sorry, we're experiencing problems with database.")
        return 1
    except:
        print("An unexpected error occurred. For more information see the log file.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())