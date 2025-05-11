# Concept for a Data Processing Framework

Components
- Database: Postgres
- Jobs: PythonRQ
- API: FastAPI

Non-Goals
- Many dependencies
- Use of an ORM

## TODOs:
v0.1
- make basic docker compose with postgres, redis, and rq worker
- add basic jobs to read, write and transform dummy data.
- add periodic scheduling

v0.2
- add ui to view running jobs
- add Job decorator with period
- add Pipeline class

v0.3
- add self-generating APIs using tables schemas

v0.4
- add API tokens