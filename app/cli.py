import uuid
import random
from datetime import datetime, timedelta
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection

# Connect to the Cassandra cluster
# cluster = Cluster(connection_class=AsyncioConnection)
# session = cluster.connect("testdb")

cluster = Cluster(['localhost'])
session = cluster.connect('testdb')

# Define some example KPI names and tags
kpi_names = ['CPU Usage', 'Memory Usage', 'Disk I/O', 'Network Throughput']
tags_list = ['critical', 'warning', 'info']


# Function to generate a random datetime within the last 30 days
def random_date():
    start = datetime.now() - timedelta(days=90)
    end = datetime.now()
    return start + (end - start) * random.random()

# kpi_name
# timestamp
# value
# tags


# Insert a large amount of data
for _ in range(10000):  # Insert 10,000 rows as an example

    kpi_name = random.choice(kpi_names)
    timestamp = random_date()
    value = round(random.uniform(0, 100), 2)
    tags = random.choice(tags_list)

    session.execute("""
    INSERT INTO kpis (kpi_name, timestamp, value, tags)
    VALUES (%s, %s, %s, %s)
    """, (kpi_name, timestamp, value, tags))

print("Data insertion complete.")
