# QuestionAnsweringSystem

## Get started:
1. Make sure you have all dependencies you need using `requirements.txt`
2. Create sample database running `create_source_db.sql`
3. You will also need two tables with locations, so first run `locations.sql`, after that run `location_relations.sql`

## Contents:

attribute_utils        -- parsing question

database_utils         -- get data from db using the information from parsed questions

src                    -- logic and working part

main.py                -- to run on some predefined number of test questions (you may use src/console_prototype.py to ask your own ones)
