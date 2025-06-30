import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

from analytics import (
    parse_tasks,
    throughput_by_team,
    throughput_by_month,
    throughput_by_team_month,
    average_lead_time,
)


def generate_html(tasks):
    html = ["<html><head><title>IT Efficiency Metrics</title></head><body>"]
    html.append("<h1>IT Efficiency Metrics</h1>")

    html.append("<h2>Throughput by team</h2><ul>")
    for team, count in throughput_by_team(tasks).items():
        html.append(f"<li>{team}: {count} tasks</li>")
    html.append("</ul>")

    html.append("<h2>Throughput by month</h2><ul>")
    for month, count in sorted(throughput_by_month(tasks).items()):
        html.append(f"<li>{month}: {count} tasks</li>")
    html.append("</ul>")

    html.append("<h2>Throughput by team by month</h2>")
    html.append("<ul>")
    for team, months in throughput_by_team_month(tasks).items():
        month_counts = ", ".join(f"{m}:{c}" for m, c in sorted(months.items()))
        html.append(f"<li>{team}: {month_counts}</li>")
    html.append("</ul>")

    html.append(f"<p>Average lead time: {average_lead_time(tasks):.1f} days</p>")
    html.append("</body></html>")
    return "\n".join(html)


class MetricsHandler(BaseHTTPRequestHandler):
    tasks = []

    def do_GET(self):
        content = generate_html(self.tasks)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web interface for IT metrics")
    parser.add_argument("tasks", help="CSV file with tasks")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    MetricsHandler.tasks = parse_tasks(args.tasks)
    httpd = HTTPServer(("0.0.0.0", args.port), MetricsHandler)
    print(f"Serving on http://localhost:{args.port}")
    httpd.serve_forever()
