'''
1 Parse server/log files for errors or patterns.
2 Generate a summary report.

Optional: highlight critical logs with colors (rich library).
'''
import os.path
import json

print("\n" * 2)

# Setting up so py reads from .log file in the specified folder
# dynamic
#folder_path = input("Enter the folder path containing the .log file: ").strip()
#log_filename = input("Enter the .log filename (e.g., server.log): ").strip()
# static
folder_path = "tests/ttest-files/"
log_filename = "fake-data.log"
log_path = os.path.join(folder_path, log_filename)
line_cnt = 0
counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
unique_errors = set()

# Check if file exists
if not os.path.isfile(log_path):
    print(f"Log file not found: {log_path}")
    exit(1)

with open(log_path, 'r') as log_file:
    log_lines = log_file.readlines()
    for line in log_lines:
        line_cnt = line_cnt + 1
        parts = line.split()
        line_status = parts[3]
        counts[line_status] = counts.get(line_status, 0) + 1
        if "ERROR" in line_status:
            error_string = " ".join(line.split()[5:])
            unique_errors.add(error_string)
        # Save last log time (assume first two columns are date and time)
        last_log_time = f"{parts[0]} {parts[1].split(',')[0]}" 
                

# Output Messsage
print("\nLog Summary\n-----------")
print("Total lines: ", line_cnt)
print("INFO:", counts["INFO"])
print("WARNING:", counts["WARNING"])
print("ERROR: ", counts["ERROR"])

print("\nUnique Errors:")
for ele in unique_errors: print("-" , ele)

print("\nLast log entry:" , line.split()[0], line.split()[1].split(",")[0])

json_output = {
    "total_lines": line_cnt,
    "counts": counts,
    "unique_errors": sorted(list(unique_errors)),
    "last_log_time": last_log_time
}

print(json.dumps(json_output, indent=2))

'''
Potential Bottlenecks

1 Disk I/O
Reading a massive file line by line can dominate runtime.
Solution: buffered reads (Python does this already), or process in chunks.

2 String Searches (in)
Checking "INFO" in line is cheap, but done billions of times it adds up.
Solution: regex or more structured log formats (e.g., JSON logs).

3 Memory Usage
Storing too much in memory (e.g., saving every parsed line).
Solution: only keep counters + sets, stream results instead of keeping all.

4 Set Growth
If there are many unique error messages (millions), the set can become memory-heavy.
Solution: limit stored messages, or count unique IDs/hashes instead.

5 Single-threaded execution
Python will process line by line on one CPU core.
Solution: parallelize (e.g., split file by chunks, multiprocessing).
'''

# How SRE teams scale log parsing in production:
#
# 1. Centralized Logging
#    - Logs are shipped to a service like ELK (Elasticsearch + Logstash + Kibana),
#      Grafana Loki, or Fluentd/Fluent Bit.
#    - Parsing happens once at ingestion, then logs are indexed and queryable.
#
# 2. Structured Logs
#    - Apps log in JSON or another structured format.
#    - No need for substring search ("INFO" in line) → direct field lookup (log["level"]).
#
# 3. Streaming Pipelines
#    - For very large log volumes, use stream processors like Kafka + Flink or Spark.
#    - Example: count errors per service per minute in real time.
#
# 4. Storage & Retention
#    - Logs stored in object storage (S3, GCS, etc.) in compressed formats (Parquet/ORC).
#    - Query on demand with engines like Athena or BigQuery.
#
# 5. Alerting & Metrics
#    - Parse logs into metrics (error rate, latency, etc.).
#    - Feed into Prometheus + Alertmanager to trigger alerts on thresholds.
#
# 6. Scalability Techniques
#    - Parallel parsing: split logs into chunks, process with multiple workers.
#    - Batch processing: aggregate per chunk, then merge results.
#    - Indexing: preprocess logs so queries are fast (e.g., Elasticsearch).