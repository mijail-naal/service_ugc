PSQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS %s (
    id serial,
    user_id VARCHAR(256) NOT NULL,
    movie_id VARCHAR(256) NOT NULL,
    viewed_frame INTEGER NOT NULL
);
"""

VERTICA_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS %s (
    id IDENTITY,
    user_id VARCHAR(256) NOT NULL,
    movie_id VARCHAR(256) NOT NULL,
    viewed_frame INTEGER NOT NULL
);
"""

CLICKHOUSE_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS %s (
    id Int64,
    user_id VARCHAR(256) NOT NULL,
    movie_id VARCHAR(256) NOT NULL,
    viewed_frame INTEGER NOT NULL
)
Engine=MergeTree()
ORDER BY id;
"""

INSERT = 'INSERT INTO %s (user_id, movie_id, viewed_frame) VALUES '

SELECT = 'SELECT count(*) FROM %s;'
