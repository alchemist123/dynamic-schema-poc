from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Define schemas
schemas = ["schema1", "schema2", "schema3", "hello"]

# Function to create User models dynamically for different schemas
def create_user_model(schema_name):
    class_name = f"User_{schema_name}"  # Unique class name
    return type(
        class_name,
        (AsyncAttrs, Base),
        {
            "__tablename__": "users",
            "__table_args__": {"schema": schema_name},
            "id": Column(Integer, primary_key=True, index=True),
            "name": Column(String, index=True),
            "email": Column(String, index=True),
        },
    )

# Create models dynamically
user_models = {schema: create_user_model(schema) for schema in schemas}
