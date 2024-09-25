CREATE_EVENT_TABLE = """
CREATE TABLE IF NOT EXISTS {database}.events (
    user_id String,
    action String,
    description String,
    event_time String,
    start_time String,
    end_time String,
)
Engine=MergeTree()
ORDER BY user_id
"""

EVENT_COLUMNS = 'user_id, action, description, event_time, start_time, end_time'
