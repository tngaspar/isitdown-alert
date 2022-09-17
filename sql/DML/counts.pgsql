/* Counts number of 
    - total request
    - failed requests
    - successful requests
*/

SELECT 
COUNT(is_up) total_count,
COUNT(case when is_up IS FALSE then is_up END) count_failed,
COUNT(case when is_up IS TRUE then is_up END) count_successful
FROM cron.history