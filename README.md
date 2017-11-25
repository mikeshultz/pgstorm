# pgstorm

PostgreSQL load testing tool with real world tests.

## Usage

    usage: pgstorm [-h] [-t N] [-d DELAY] [-l LEVEL] [-y TYPE] [-v VALUE]
                   DSN [FILE]

    PostgreSQL load testing.

    positional arguments:
      DSN                   pg connection string (default:
                            postgresql://localhost:5432/postgres)
      FILE                  sql file to run(or stdin)

    optional arguments:
      -h, --help            show this help message and exit
      -t N, --threads N     amount of threads to start
      -d DELAY, --delay DELAY
                            thread health check delay in seconds(default: 0.05)
      -l LEVEL, --log-level LEVEL
                            log level(default: WARNING)
      -y TYPE, --type TYPE  test type M - Must have results, N - Must return
                            --value rows, E - Equal too --value
      -v VALUE, --value VALUE
                            value comparison for test type

## Examples 

### Run SQL File

    pgstorm -t 5 postgresql://localhost:5432/mydb mytest.sql

### Require Any Results

    echo "SELECT TRUE FROM \"user\" WHERE usename = 'mike';" | pgstorm -y M postgresql://localhost:5432/mydb 

### Require Row Count

    pgstorm -y N -v 3 postgresql://localhost:5432/mydb return_three_rows.sql

### Require Value

You may want to check against an exact value to make sure you're getting 
consistent results.

For instance, you want to make sure you always get `record_id` = 153:

    echo "SELECT record_id FROM records WHERE name = 'Jones';" | pgstorm -y E -v 153 postgresql://localhost:5432/mydb get_user.sql 