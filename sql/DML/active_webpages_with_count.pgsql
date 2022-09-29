SELECT 
    dw.tag
    ,dw.url
    ,dw.interval 
    ,count(h.url) num_checks
FROM cron.dim_webpages dw
LEFT JOIN cron.history h on dw.url = h.url
GROUP BY dw.tag, dw.url, dw.interval