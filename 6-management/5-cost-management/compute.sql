show compute pools;
select * from table(result_scan())
where "state" <> 'SUSPENDED';

alter compute pool cpu suspend;

--  hourly consumption for SPCS only
-- (line chart credit_used w/ start_time)
select *
from SNOWFLAKE.ACCOUNT_USAGE.SNOWPARK_CONTAINER_SERVICES_HISTORY;

select *
from SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY
where service_type = 'SNOWPARK_CONTAINER_SERVICES';

select *
from SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
where service_type = 'SNOWPARK_CONTAINER_SERVICES';

select *
from SNOWFLAKE.ORGANIZATION_USAGE.METERING_DAILY_HISTORY
where service_type = 'SNOWPARK_CONTAINER_SERVICES';
