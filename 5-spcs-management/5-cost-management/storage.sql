-- image repositories are also here! (w/ NULL stage_type)
select *
from SNOWFLAKE.ACCOUNT_USAGE.STAGES;

-- for block volume storage or snapshots
select *
from SNOWFLAKE.ACCOUNT_USAGE.BLOCK_STORAGE_HISTORY;

-- for all stages (cannot filter)
select *
from SNOWFLAKE.ACCOUNT_USAGE.STAGE_STORAGE_USAGE_HISTORY;

-- w/ stage bytes, but for all stages (cannot filter)
select *
from SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE;

-- w/ bytes in/out
select *
from SNOWFLAKE.ACCOUNT_USAGE.SPCS_EGRESS_ACCESS_HISTORY;

-- only for Business Critical
select *
from SNOWFLAKE.ACCOUNT_USAGE.OUTBOUND_PRIVATELINK_ENDPOINTS;
