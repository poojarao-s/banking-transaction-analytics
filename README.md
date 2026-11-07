# Banking Transaction Reliability & Anomaly Detection

### End-to-End Banking Analytics Portfolio Project

**Technologies:** Python | Pandas | PostgreSQL | SQL | Tableau | GitHub

[**View Interactive Tableau Dashboard**](https://public.tableau.com/views/BankingTransactionReliabilityDashboard/BankingTransactionReliabilityDashboard)

## Project Overview

This project analyzes 50,000 synthetically generated banking transactions to evaluate payment reliability, identify transaction failure patterns, investigate processing-time outliers, and detect repeated payment references.

The objective is to demonstrate how transaction-level data can be transformed into actionable business insights using Python, PostgreSQL, and Tableau.

## Business Questions

- Which payment channels experience the highest transaction failure rates?
- What are the most common reasons for failed payments?
- Do processing times reveal unusually delayed transactions?
- How frequently do payment references appear more than once?
- How can payment operations teams use these findings to prioritize further investigation?

## Dataset

The project uses 50,000 synthetic banking transaction records containing transaction identifiers, payment references, customer identifiers, payment channels, transaction amounts, processing times, statuses, and failure reasons.

All data is simulated and does not contain real customer information or represent actual bank performance.

## Tools and Methodology

**Python & Pandas:** Generated synthetic transaction data, analyzed failure rates, investigated processing-time distributions, and identified repeated payment references.

**PostgreSQL & SQL:** Validated transaction metrics, calculated channel-level failure rates, grouped repeated payment references, and used window functions to analyze transaction timing.

**Tableau:** Developed an interactive dashboard featuring KPI indicators, channel-level failure analysis, failure reasons, processing-time distributions, and repeated-reference monitoring.

## Key Findings

| Metric | Result |
|---|---:|
| Total transactions | 50,000 |
| Failed transactions | 2,296 |
| Overall failure rate | 4.59% |
| API channel failure rate | 6.57% |
| Transactions exceeding 30 seconds | 20,410 |
| Median processing time | 26 seconds |
| 99th-percentile processing time | 727 seconds |
| Repeated payment references | 299 |
| Records involving repeated references | 599 |

### Business Insights

**Payment Channel Reliability:** API transactions experienced the highest failure rate at 6.57%, compared with 2.96% for Branch transactions. This suggests prioritizing investigation of API payment flows.

**Failure Patterns:** Insufficient funds accounted for 609 failed transactions, followed by validation errors (581), timeouts (574), and bank rejections (532).

**Processing-Time Outliers:** Although median processing time was 26 seconds, the 99th percentile reached 727 seconds, indicating a substantial long tail of simulated processing delays.

**Repeated References:** A total of 299 payment references appeared multiple times, involving 599 transaction records. These occurrences are potential review candidates, not confirmed duplicate charges or fraudulent transactions.

## Recommendations

1. Investigate API channel validation, timeout, and rejection patterns to understand the causes of its comparatively high failure rate.
2. Monitor processing-time percentiles alongside average latency to identify extreme delays.
3. Establish operational review procedures for repeated payment references, including timestamp, status, and payment-context checks.
4. Define appropriate service-level targets before classifying slow transactions as SLA violations.

## Interactive Dashboard

[Explore the Tableau Dashboard](https://public.tableau.com/views/BankingTransactionReliabilityDashboard/BankingTransactionReliabilityDashboard)

The dashboard includes interactive channel filtering, transaction reliability KPIs, payment failure analysis, processing-time visualization, and repeated-reference monitoring.

## Limitations

This is a synthetic portfolio project. Its patterns are simulated and should not be interpreted as empirical findings about banking operations. The 30-second processing threshold is exploratory rather than an established banking SLA. Repeated references alone do not prove duplicate payments or fraud.

## Repository Structure

```text
banking-transaction-analytics/
├── data/
│   └── transactions.csv
├── scripts/
│   ├── generate_transactions.py
│   └── analyze_transactions.py
├── sql/
│   ├── 01_transaction_overview.sql
│   ├── 02_channel_failure_analysis.sql
│   └── 03_duplicate_payment_analysis.sql
└── README.md
```

## Project Outcome

This project demonstrates an end-to-end analytics workflow—from generating and exploring transaction data to validating metrics with SQL and communicating findings through an interactive Tableau dashboard.

It highlights practical skills in data analysis, SQL window functions, KPI development, anomaly investigation, data visualization, and business-oriented analytical communication.
