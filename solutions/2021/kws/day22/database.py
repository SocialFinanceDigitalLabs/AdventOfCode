import sqlite3
from contextlib import contextmanager
from tempfile import  NamedTemporaryFile


def _get_points(xrange, yrange, zrange):
    for x in range(xrange[0], xrange[1] + 1):
        for y in range(yrange[0], yrange[1] + 1):
            for z in range(zrange[0], zrange[1] + 1):
                yield x, y, z


class Database:

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)

        # Create table if not exists
        self.conn.execute('''CREATE TABLE IF NOT EXISTS cubes (
            x INTEGER,
            y INTEGER,
            z INTEGER,
            value INTEGER,
            PRIMARY KEY (x, y, z)
            )
        ''')

    def set_value(self, x, y, z, value):
        if value == 0:
            self.conn.execute('DELETE FROM cubes WHERE x=? AND y=? AND z=?', (x, y, z))
        else:
            self.conn.execute('INSERT OR REPLACE INTO cubes (x, y, z, value) VALUES (?,?,?,?)', (x, y, z, value))

    def set_many(self, xrange, yrange, zrange, value):
        print(f'Setting many values to {value}')
        if value == 0:
            self.conn.execute('DELETE FROM cubes WHERE x>=? AND x<=? AND y>=? AND y<=? AND z>=? AND z<=?',
                              (xrange[0], xrange[1], yrange[0], yrange[1], zrange[0], zrange[1]))
        else:
            points = []
            count = 0
            for pt in _get_points(xrange, yrange, zrange):
                points.append(pt)
                count += 1
                if len(points) > 10000:
                    self.conn.executemany('INSERT OR REPLACE INTO cubes (x, y, z, value) VALUES (?,?,?,1)', points)
                    points = []
                if count % 1000000 == 0:
                    print("Written {} points".format(count))
            self.conn.executemany('INSERT OR REPLACE INTO cubes (x, y, z, value) VALUES (?,?,?,1)', points)


    def close(self):
        self.conn.close()

    @staticmethod
    @contextmanager
    def open(filename=None):
        tmpfile = None
        if filename is None:
            tmpfile = NamedTemporaryFile()
            filename = tmpfile.name
        db = None
        try:
            db = Database(filename)
            yield db
        finally:
            if db is not None:
                db.close()
            if tmpfile is not None:
                tmpfile.close()

    def count_values(self, value):
        cur = self.conn.cursor()
        cur.execute('SELECT COUNT(*) FROM cubes WHERE value=?', (value,))
        return cur.fetchone()[0]