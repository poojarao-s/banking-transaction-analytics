
SELECT
    channel,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (
        WHERE LOWER(TRIM(status)) = 'failed'
    ) AS failed_transactions,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE LOWER(TRIM(status)) = 'failed'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS failure_rate
FROM transactions
GROUP BY channel
ORDER BY failure_rate DESC;
