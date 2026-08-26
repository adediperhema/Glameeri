# =========================================================================
# 📦 RUN ONCE: AUTO-CREATE EXTENDED MEASUREMENTS LEDGER TABLES (DB_INIT.PY)
# =========================================================================
from database import engine, Base, User, ClientMeasurement

print("🧱 Scanning database model blueprints...")
# This reads all tables linked to your Base class and generates missing entries instantly!
Base.metadata.create_all(bind=engine)
print("🎉 Success! Table 'client_measurements' is fully active on Port 5432.")
