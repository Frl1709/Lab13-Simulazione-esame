from database.DB_connect import DBConnect
from model.state import State


class DAO():
    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(extract(year from datetime)) as year
                    from sighting"""

        cursor.execute(query,)
        for row in cursor:
            result.append((row['year']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShapes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape
                    from sighting
                    where shape != ""
                    """

        cursor.execute(query, )
        for row in cursor:
            result.append((row['shape']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStates():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from state
                        """

        cursor.execute(query, )
        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnectionWeighted(idMap, forma, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select n.state1, n.state2, COUNT(*) as N
                    from neighbor n , sighting s
                    where s.shape = %s and extract(year from s.`datetime`) = %s
                    and n.state1 < n.state2 and (upper(s.state) = n.state1 or  upper(s.state) = n.state2)
                    group by n.state1, n.state2  
                        """

        cursor.execute(query, (forma, anno,))
        for row in cursor:
            result.append((idMap[row['state1']],
                           idMap[row['state2']],
                           row['N']))

        cursor.close()
        conn.close()
        return result
