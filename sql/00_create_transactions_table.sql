
-- Banking Transaction Reliability & Anomaly Detection
-- Create table for the synthetic transaction dataset

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    payment_reference VARCHAR(20),
    customer_id VARCHAR(20),
    created_at TIMESTAMP,
    channel VARCHAR(30),
    payment_type VARCHAR(50),
    amount_usd NUMERIC(12,2),
    status VARCHAR(20),
    processing_seconds INTEGER,
    failure_reason VARCHAR(50),
    is_simulated_duplicate BOOLEAN
);
