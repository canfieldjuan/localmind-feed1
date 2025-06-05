from replit import db

MEMORY_LIMIT = 10

def get_context(session_id, agent):
    memory_key = f"memory:{session_id}:{agent}"
    return db.get(memory_key, [])

def update_context(session_id, agent, message):
    memory_key = f"memory:{session_id}:{agent}"
    context = db.get(memory_key, [])
    context.append(message)
    db[memory_key] = context[-MEMORY_LIMIT:]

def reset_all_memory():
    keys = [k for k in db.keys() if k.startswith("memory:")]
    for k in keys:
        del db[k]

def get_all_logs():
    return {k: db[k] for k in db.keys() if k.startswith("memory:")}
