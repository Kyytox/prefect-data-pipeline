{{ config(materialized='view') }}

SELECT * FROM public.raw_rockets