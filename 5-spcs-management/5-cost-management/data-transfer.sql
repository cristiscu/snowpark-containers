-- outbound (~upload image in repo)
-- (line chart w/ bytes_transferred on start_time)
select * 
from SNOWFLAKE.ACCOUNT_USAGE.DATA_TRANSFER_HISTORY
where transfer_type = 'SNOWPARK_CONTAINER_SERVICES';

-- internal
select *
from SNOWFLAKE.ACCOUNT_USAGE.INTERNAL_DATA_TRANSFER_HISTORY;
-- where service_type = 'SERVICE_FUNCTION';

select *
from SNOWFLAKE.ACCOUNT_USAGE.DATA_TRANSFER_HISTORY
where transfer_type = 'INTERNAL';

select *
from SNOWFLAKE.ORGANIZATION_USAGE.DATA_TRANSFER_HISTORY
where transfer_type = 'INTERNAL';

select *
from SNOWFLAKE.ORGANIZATION_USAGE.DATA_TRANSFER_DAILY_HISTORY
where service_type = 'INTERNAL_DATA_TRANSFER';

select *
from SNOWFLAKE.ORGANIZATION_USAGE.RATE_SHEET_DAILY
where service_type = 'INTERNAL_DATA_TRANSFER';

select *
from SNOWFLAKE.ORGANIZATION_USAGE.USAGE_IN_CURRENCY_DAILY
where service_type = 'INTERNAL_DATA_TRANSFER';
