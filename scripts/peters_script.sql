WITH
	insights AS (
		SELECT user_name, COUNT(DISTINCT (npi)) AS count1
		FROM insights_views.sfdc_contact_contactinfo con
		LEFT JOIN insights_views.sfdc_user_userinfo u ON (con.owner_id = u.user_id)
		GROUP BY 1
		ORDER BY 2 ASC
	),
	dim      AS (
		SELECT (dpm_first_name || ' ' || dpm_last_name) AS dpm_name,
		       COUNT(DISTINCT (provider_npi))           AS assigned_providers
		FROM capsule_dw.fact_provider fpro
		INNER JOIN capsule_dw.dim_provider dpro USING (dim_provider_key)
		INNER JOIN capsule_dw.dim_dpm ddpm USING (dim_dpm_key)
		WHERE fpro.is_active = TRUE AND dpro.is_active = TRUE AND ddpm.is_active = TRUE
		GROUP BY 1
		ORDER BY 2 ASC
	)

SELECT user_name
	 , count1                    AS insights_count
	 , assigned_providers         AS dim_count
	 , dim_count - insights_count AS diff
FROM insights
LEFT JOIN dim ON user_name = dpm_name
where diff != 0
ORDER BY diff