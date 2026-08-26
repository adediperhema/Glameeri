# =========================================================================
# 🧵 WORKSPACE PATCH: ALTER USER TABLE METRIC COLUMNS (PATCH_DB.PY) 🧵
# =========================================================================
from typing import Any

import psycopg2


def migrate_subscription_columns():
    print("⏳ Connecting to your PostgreSQL cluster instance on Port 5432...")
    try:
        # Link using your unconflicted trusted loopback configuration credentials
        raw_connection = psycopg2.connect(
            user="postgres",
            password="rhema12345",
            host="127.0.0.1",
            port="5432",
            database="Fashiondb",
        )

        conn: Any = raw_connection
        conn.autocommit = True
        # =========================================================================
        # 🪡 FIX: TYPE-SAFE NATIVE PSYCOPG2 CURSOR INITIALISATION (PATCH_DB.PY) 🪡
        # =========================================================================

        # BEFORE: cursor = conn.connect().cursor() if hasattr(conn, "connect") else conn.cursor()
        # 🔥 FIXED: Call .cursor() directly on the connection handle. Wipes out the red line!
        cursor = conn.cursor()

        # cursor = conn.connect().cursor()
        # if hasattr(conn, "connect") else conn.cursor()

        print("🧱 Injecting subscription column schemas into live 'users' table...")

        # 🔥 ALTER PASS A: Add subscription tier defaults cleanly to freemium
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR NOT NULL DEFAULT 'freemium';
        """)

        # 🔥 ALTER PASS B: Add monthly generation rolling integer tracking fields
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS monthly_generation_count INTEGER NOT NULL DEFAULT 0;
        """)

        # 🔥 ALTER PASS C: Add timezone aware cycle reset timing metrics
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS cycle_reset_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
        """)

        print(
            "🎉 SUCCESS! Missing user table column footprints synchronized flawlessly."
        )
        cursor.close()
        conn.close()
    except Exception as err:
        print(f"❌ Migration pass aborted: {err}")


if __name__ == "__main__":
    migrate_subscription_columns()
