import argparse
import csv
from collections import defaultdict
from datetime import datetime
from statistics import mean

DATE_FORMAT = "%Y-%m-%d"


def parse_tasks(path):
    tasks = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = datetime.strptime(row["start_date"], DATE_FORMAT)
            end = datetime.strptime(row["end_date"], DATE_FORMAT)
            tasks.append({
                "team": row["team"],
                "task_id": row["task_id"],
                "start": start,
                "end": end,
                "lead_time": (end - start).days,
            })
    return tasks


def throughput_by_team(tasks):
    result = defaultdict(int)
    for t in tasks:
        result[t["team"]] += 1
    return result


def throughput_by_month(tasks):
    result = defaultdict(int)
    for t in tasks:
        key = t["end"].strftime("%Y-%m")
        result[key] += 1
    return result


def throughput_by_team_month(tasks):
    result = defaultdict(lambda: defaultdict(int))
    for t in tasks:
        month = t["end"].strftime("%Y-%m")
        result[t["team"]][month] += 1
    return result


def average_lead_time(tasks):
    if not tasks:
        return 0
    return mean(t["lead_time"] for t in tasks)


def report(tasks):
    print("Throughput by team:")
    for team, count in throughput_by_team(tasks).items():
        print(f"  {team}: {count} tasks completed")
    print()
    print("Throughput by month:")
    for month, count in sorted(throughput_by_month(tasks).items()):
        print(f"  {month}: {count} tasks completed")
    print()
    print("Throughput by team by month:")
    for team, months in throughput_by_team_month(tasks).items():
        month_counts = ", ".join(f"{m}:{c}" for m, c in sorted(months.items()))
        print(f"  {team}: {month_counts}")
    print()
    print(f"Average lead time: {average_lead_time(tasks):.1f} days")


def main():
    parser = argparse.ArgumentParser(description="Simple IT efficiency metrics")
    parser.add_argument("tasks", help="CSV file with tasks")
    args = parser.parse_args()
    tasks = parse_tasks(args.tasks)
    report(tasks)


if __name__ == "__main__":
    main()
