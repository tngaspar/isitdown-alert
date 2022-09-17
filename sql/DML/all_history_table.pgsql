SELECT tag, url, request_time, is_up 
FROM cron.history
ORDER BY request_time DESC;