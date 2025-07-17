{{config(materialized='table')}}

WITH rocket_launches AS (
	SELECT
		country,
		COUNT(*) AS nb_launches,
		SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS nb_success
	FROM {{ ref('stg_rockets') }}
	GROUP BY country
	ORDER BY nb_launches DESC
)

SELECT
	country,
	nb_launches,
	nb_success
FROM rocket_launches