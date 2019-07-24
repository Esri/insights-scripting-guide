## Database Connection Examples

**Microsoft Access using pyodbc**


```
# make sure pyodbc package is installed
# import pyodbc driver 
# make sure python and access versions are the same 
# both should be 32 bit or 64 bit
import pyodbc
# import pandas to create dataframe 
import pandas as pd

# create connection string for driver and path to access database
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\test_data\AAPL.mdb;")
# query to get all records from AAPL table in access db
query = 'select * from table_name;'
# create pandas dataframe from table data
df = pd.read_sql(query, conn)
df

```


**PostgreSQL using psycopg2**

```
# make sure psycopg2 is installed
# import psycopg2 driver
import psycopg2
# import pandas to create dataframe
import pandas as pd

# change named objects to fit specific instance
host = "database_host_name"
user = "user"
dbname = "database_name"
password = "password"
sslmode = "require"
# build database connection string
conn_string = "host={} user={} dbname={} password={} sslmode={}".format(host, user, dbname, password, sslmode)
# make database connection
conn = psycopg2.connect(conn_string)
# create pandas dataframe from table data
df = pd.read_sql('select * from table_name', con=conn)
df
```

**Terradata using SQLAlchemy**

 ```
# make sure proper Teradata driver is installed
# make sure SQLAlchemy is installed
from sqlalchemy import create_engine
# import pandas to create dataframe
import pandas as pd

# change named objects to fit specific instance
user = "user"
password = "password" 
host = "hostname"
# make database connection
engine = create_engine("teradata://{}:{}@{}:22/".format(user, password, host))
# execute sql to get records from table
query = 'select * from table_name'
query_result = engine.execute(query)

# create pandas dataframe from table data
df = pd.read_sql(query, engine)
df 
 ```




 ```
