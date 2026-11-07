
import pandas as pd
from pathlib import Path

# Find the dataset
project_folder = Path(__file__).resolve().parent.parent
csv_path = project_folder / "data" / "transactions.csv"

# Load transactions
df = pd.read_csv(csv_path)

# Calculate transaction metrics
total_transactions = len(df)

failed_transactions = (
    df["status"].astype(str).str.strip().str.lower() == "failed"
).sum()

failure_rate = (failed_transactions / total_transactions) * 100

# Display results
print(f"Total transactions: {total_transactions:,}")
print(f"Failed transactions: {failed_transactions:,}")
print(f"Failure rate: {failure_rate:.2f}%")


# Analyze transaction failures by payment channel

df["is_failed"] = (
    df["status"].astype(str).str.strip().str.lower() == "failed"
)

channel_analysis = df.groupby("channel").agg(
    total_transactions=("transaction_id", "count"),
    failed_transactions=("is_failed", "sum")
)

channel_analysis["failure_rate"] = (
    channel_analysis["failed_transactions"]
    / channel_analysis["total_transactions"]
    * 100
)

channel_analysis = channel_analysis.sort_values(
    by="failure_rate",
    ascending=False
)

print("\nTransaction Failure Analysis by Channel:")
print(channel_analysis.round(2).to_string())


# Step 10: Investigate failure reasons

failed_df = df[df["is_failed"]].copy()

# Count failures by reason
failure_reasons = (
    failed_df.groupby("failure_reason", dropna=False)
    .size()
    .sort_values(ascending=False)
)

print("\nFailure Reasons:")
print(failure_reasons.to_string())

# Investigate failure reasons across channels
failure_by_channel = pd.crosstab(
    failed_df["channel"],
    failed_df["failure_reason"],
    dropna=False
)

print("\nFailure Reasons by Channel:")
print(failure_by_channel.to_string())


# Step 11: Failure rates by reason and channel

# Total transactions per channel
channel_totals = df.groupby("channel").size()

# Failure counts by channel and reason
reason_counts = pd.crosstab(
    failed_df["channel"],
    failed_df["failure_reason"]
)

# Divide by all transactions in that channel
reason_rates = reason_counts.div(
    channel_totals,
    axis=0
) * 100

print("\nFailure Rates by Reason and Channel (%):")
print(reason_rates.round(2).to_string())


# Step 12: Processing time analysis

# Convert processing time into numeric values
df["processing_seconds"] = pd.to_numeric(
    df["processing_seconds"],
    errors="coerce"
)

# Flag transactions taking longer than 30 seconds
df["is_slow"] = df["processing_seconds"] > 30

# Calculate processing metrics by channel
processing_analysis = df.groupby("channel").agg(
    total_transactions=("transaction_id", "count"),
    average_seconds=("processing_seconds", "mean"),
    median_seconds=("processing_seconds", "median"),
    p95_seconds=("processing_seconds", lambda x: x.quantile(0.95)),
    slow_transactions=("is_slow", "sum")
)

# Calculate slow transaction rate
processing_analysis["slow_rate"] = (
    processing_analysis["slow_transactions"]
    / processing_analysis["total_transactions"]
    * 100
)

# Sort by the highest slow transaction rate
processing_analysis = processing_analysis.sort_values(
    by="slow_rate",
    ascending=False
)

print("\nProcessing Time Analysis by Channel:")
print(processing_analysis.round(2).to_string())


# Step 13: Investigate processing time outliers

print("\nProcessing Time Distribution:")

print(
    df["processing_seconds"].describe(
        percentiles=[0.50, 0.90, 0.95, 0.99, 0.999]
    ).round(2)
)

print("\n10 Slowest Transactions:")

slowest = df.nlargest(
    10, "processing_seconds"
)[
    [
        "transaction_id",
        "channel",
        "status",
        "processing_seconds",
        "failure_reason"
    ]
]

print(slowest.to_string(index=False))


# Step 14: Investigate repeated payment references

# Count records associated with each payment reference
reference_counts = df["payment_reference"].value_counts()

# Identify references appearing more than once
repeated_references = reference_counts[
    reference_counts > 1
]

print("\nRepeated Payment Reference Analysis:")
print(f"Unique payment references: {df['payment_reference'].nunique():,}")
print(f"References appearing more than once: {len(repeated_references):,}")
print(f"Records associated with repeated references: {repeated_references.sum():,}")

# Display sample records for repeated references
repeated_records = df[
    df["payment_reference"].isin(repeated_references.index)
].sort_values(["payment_reference", "created_at"])

print("\nSample Repeated Payment Records:")

print(
    repeated_records[
        [
            "transaction_id",
            "payment_reference",
            "customer_id",
            "created_at",
            "amount_usd",
            "status"
        ]
    ].head(12).to_string(index=False)
)

# Step 15: Classify repeated payment references

# Work only with records that share a payment reference
repeated_df = df[
    df["payment_reference"].isin(repeated_references.index)
].copy()

# Identify completed records
repeated_df["is_completed"] = (
    repeated_df["status"].astype(str).str.strip().str.lower()
    == "completed"
)

# Summarize each payment reference
reference_summary = repeated_df.groupby(
    "payment_reference"
).agg(
    total_records=("transaction_id", "count"),
    completed_records=("is_completed", "sum"),
    first_seen=("created_at", "min"),
    last_seen=("created_at", "max")
)

# Classify each reference
def classify_reference(row):
    if row["completed_records"] >= 2:
        return "Multiple Completed"
    elif row["completed_records"] == 1:
        return "One Completed"
    else:
        return "No Completed"

reference_summary["classification"] = (
    reference_summary.apply(classify_reference, axis=1)
)

print("\nRepeated Reference Classification:")
print(
    reference_summary["classification"]
    .value_counts()
    .to_string()
)

print("\nExamples of Multiple Completed References:")
print(
    reference_summary[
        reference_summary["classification"] == "Multiple Completed"
    ].head(10).to_string()
)


# Step 16: Analyze timing of repeated payment references

# Convert timestamps to datetime
repeated_df["created_at"] = pd.to_datetime(
    repeated_df["created_at"]
)

# Sort each payment reference chronologically
repeated_df = repeated_df.sort_values(
    ["payment_reference", "created_at"]
)

# Calculate the gap between consecutive records
repeated_df["hours_since_previous"] = (
    repeated_df.groupby("payment_reference")["created_at"]
    .diff()
    .dt.total_seconds() / 3600
)

# Summarize gaps across all repeated references
reference_gaps = (
    repeated_df.groupby("payment_reference")["created_at"]
    .agg(["min", "max"])
)

reference_gaps["gap_hours"] = (
    (reference_gaps["max"] - reference_gaps["min"])
    .dt.total_seconds() / 3600
)

print("\nRepeated Payment Time Gap Distribution:")
print(
    reference_gaps["gap_hours"].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95]
    ).round(2)
)

print("\nRepeated References More Than 24 Hours Apart:")
print(
    (reference_gaps["gap_hours"] > 24).sum()
)

print("\nRepeated References Within 1 Hour:")
print(
    (reference_gaps["gap_hours"] <= 1).sum()
)


# Step 17: Validate repeated-reference detection

# Our detection rule: payment reference occurs more than once
df["detected_repeated_reference"] = (
    df["payment_reference"].duplicated(keep=False)
)

# Convert the synthetic duplicate label to a boolean
df["actual_injected_duplicate"] = (
    df["is_simulated_duplicate"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["true", "1", "yes"])
)

print("\nRepeated-Reference Detection Validation:")

print(
    pd.crosstab(
        df["actual_injected_duplicate"],
        df["detected_repeated_reference"],
        rownames=["Injected Duplicate"],
        colnames=["Detected Repeated Reference"]
    ).to_string()
)

print("\nTotal injected duplicate records:")
print(df["actual_injected_duplicate"].sum())

print("\nTotal records flagged by our detection rule:")
print(df["detected_repeated_reference"].sum())


# Step 18: Check for missed injected duplicates

missed_duplicates = df[
    df["actual_injected_duplicate"]
    & ~df["detected_repeated_reference"]
]

print("\nInjected duplicates not detected:")
print(len(missed_duplicates))

# Check records flagged that aren't labeled injected
unlabeled_flagged = df[
    ~df["actual_injected_duplicate"]
    & df["detected_repeated_reference"]
]

print("\nFlagged records not labeled injected:")
print(len(unlabeled_flagged))
