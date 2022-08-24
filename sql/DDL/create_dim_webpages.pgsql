DROP TABLE IF EXISTS cron.dim_webpages;

CREATE TABLE cron.dim_webpages (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(2000),
    url VARCHAR(2000),
    interval VARCHAR(255)
);
