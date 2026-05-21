""" 
"
" TODO: add info 
"
"""
from jobs.ingest_program_member_data import run as ingest_program_member_data

# Register jobs within this tuple ("job_name", "function_name")
REGISTRY = (
    ("ingest_program_member_data", "ingest_program_member_data" ),
    ("test2", "test2" ),
)
