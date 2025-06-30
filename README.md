# IT Efficiency Assessment Tool

This repository provides a minimal prototype of a command line tool for calculating basic IT efficiency metrics.

## Features

- Parses tasks from a CSV file.
- Calculates throughput per team and per month.
- Computes average lead time.
- Shows throughput distribution by team over months.

## Usage

Run the script with a path to a CSV file with the following columns:

```
team,task_id,start_date,end_date
```

Example command:

```
python3 src/analytics.py data/sample_tasks.csv
```

This will output simple metrics to the console.
