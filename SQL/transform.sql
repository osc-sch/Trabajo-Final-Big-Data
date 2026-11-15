CREATE OR REPLACE TABLE ventas_validas AS
SELECT * FROM ventas_raw WHERE
TRY_CAST(date AS DATE) IS NOT NULL
AND region IS NOT NULL
AND TRIM(region) <> ''
AND product IS NOT NULL
AND TRIM(product) <> ''
AND channel IS NOT NULL
AND TRIM(channel) <> ''
AND units > 0
AND units IS NOT NULL
AND unit_price > 0
AND unit_price IS NOT NULL
AND revenue > 0
AND revenue IS NOT NULL;    