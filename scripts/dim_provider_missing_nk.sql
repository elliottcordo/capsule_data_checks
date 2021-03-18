with source as (
    select npi_c as npi
    from salesforce.contacts
    where last_modified_date < dateadd(HOUR, -3, getdate())
), dim as (
    select distinct provider_npi
    from capsule_dw.dim_provider
)
select source.*
from source
left join dim on npi=provider_npi
where npi is not null and provider_npi is null;