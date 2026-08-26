# =========================================================================
# 🪡 RUN ONCE: STANDALONE POSTGRESQL CLEANSE UTILITY (FIX_USER.PY) 🪡
# =========================================================================
import psycopg2


def cleanse_stale_studio_profiles():
    print("⏳ Purging corrupted database credential hashes on Port 5433...")
    try:
        # Connect using your updated trusted alternate port layout channel configuration
        conn = psycopg2.connect(
            user="postgres",
            password="rhema12345",
            host="127.0.0.1",
            port="5432",
            database="Fashiondb",
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Hard-erase any historical accounts to provide a clean slate for your updated security algorithms
        cursor.execute("TRUNCATE TABLE users CASCADE;")
        print(
            "🎉 Success! Stale, broken account rows completely wiped out of PostgreSQL tables."
        )

        cursor.close()
        conn.close()
    except Exception as err:
        print(f"❌ Cleanse execution stalled: {err}")


if __name__ == "__main__":
    cleanse_stale_studio_profiles()
