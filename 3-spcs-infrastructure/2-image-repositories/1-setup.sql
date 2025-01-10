USE ROLE ACCOUNTADMIN;
USE test.public;

-- ========================================
-- create+drop image repo
CREATE IMAGE REPOSITORY repo_tmp;
SHOW IMAGES IN IMAGE REPOSITORY repo_tmp;
DROP IMAGE REPOSITORY repo_tmp;             -- cannot drop individual images!

-- ========================================
-- create image repo
CREATE IMAGE REPOSITORY IF NOT EXISTS repo;
SHOW IMAGE REPOSITORIES;                    -- get repo URL
SHOW IMAGES IN IMAGE REPOSITORY repo;       -- call after pushing images here
