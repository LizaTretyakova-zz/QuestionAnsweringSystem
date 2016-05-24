from database_utils.base_wrapper import BaseWrapper

import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import config

logger = config.get_logger()

DEFAULT_REGION = 'World'
INVALID_REGION_ID = 0


class LocationWrapper(BaseWrapper):
    def __init__(self):
        super().__init__()

    def get_location_id(self, location: str) -> int:
        query = "SELECT id FROM locations WHERE lower(name)=%s"
        cur = self.conn.cursor()
        cur.execute(query, (location,))
        result = cur.fetchall()
        if not result:
            return [INVALID_REGION_ID]
        return [x[0] for x in result]

    def get_by_location(self, parent_location: str, target_type: int) -> list:
        # try:
        #     self.get_by_location.logger
        # except AttributeError:
        #     import sys
        #     from os.path import dirname, abspath
        #     sys.path.insert(0, dirname(dirname(abspath(__file__))))
        #     import config
        #     self.get_by_location.logger = config.get_logger()

        parent_location_id = self.get_location_id(parent_location.lower())
        query = ("SELECT locations.name\n"
                 "FROM locations\n"
                 "INNER JOIN location_relations\n"
                 "ON locations.id=location_relations.region_id\n"
                 "WHERE parent_region_id IN %s\n"
                 "AND type=%s")
        cur = self.conn.cursor()
        cur.execute(query, (tuple(parent_location_id), target_type))
        res = [x[0] for x in cur.fetchall()]
        # self.get_by_location.
        logger.debug(res)
        return res
