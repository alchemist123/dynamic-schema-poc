from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.models import Base

app = FastAPI()

@app.post("/create-schema/{schema_name}")
async def create_schema(schema_name: str, db: AsyncSession = Depends(get_db)):
    await db.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
    await db.commit()
    return {"message": f"Schema {schema_name} created successfully"}

@app.post("/run-migrations/{schema_name}")
async def run_migrations(schema_name: str):
    import subprocess
    subprocess.run(["alembic", "upgrade", "head"], env={"ALEMBIC_SCHEMA": schema_name})
    return {"message": f"Migration applied for schema {schema_name}"}
