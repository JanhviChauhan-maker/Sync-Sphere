import asyncio
from pydantic import BaseModel, Field

import sys
import os
sys.path.insert(0, os.path.abspath("./src"))

from syncsphere.identity.infrastructure.documents.user_document import UserDocument

async def run():
    print("UserDocument dict:", UserDocument.__dict__.keys())
    try:
        print(UserDocument.email)
    except Exception as e:
        print(f"Exception: {type(e).__name__} - {e}")

if __name__ == "__main__":
    asyncio.run(run())
