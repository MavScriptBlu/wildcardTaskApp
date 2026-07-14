"""
App settings live here. We pull everything from environment variables so we're not hardcoding passwords, and so the same code works whether it's running in a container or on your machine.
"""

import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://taskuser:taskpass@localhost:5432/taskdb")