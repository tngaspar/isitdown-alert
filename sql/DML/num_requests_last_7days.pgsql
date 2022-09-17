/* Count number of request in last 7 days
*/

SELECT 
    DATE(request_time) date
    ,COUNT(*) total_requests
    ,COUNT(CASE WHEN is_up IS false THEN is_up END) failed_requests
FROM cron.history
WHERE request_time >= current_date at time zone 'Z' - interval '6 days' -- 7 days including current date
GROUP BY date
ORDER BY date