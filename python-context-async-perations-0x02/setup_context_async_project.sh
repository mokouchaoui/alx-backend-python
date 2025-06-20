#!/bin/bash

# Exit script on error
set -e

echo "📁 Creating Task 0: 0-databaseconnection.py"
cat > 0-databaseconnection.py << 'EOF'
import sqlite3

class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# ✅ Usage
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
EOF

echo "📁 Creating Task 1: 1-execute.py"
cat > 1-execute.py << 'EOF'
import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or []

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# ✅ Usage
with ExecuteQuery("SELECT * FROM users WHERE age > ?", [25]) as results:
    for row in results:
        print(row)
EOF

echo "📁 Creating Task 2: 3-concurrent.py"
cat > 3-concurrent.py << 'EOF'
import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Run concurrent fetch
asyncio.run(fetch_concurrently())
EOF

echo "✅ All tasks created successfully!"
