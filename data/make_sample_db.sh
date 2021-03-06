#!/bin/bash
# Generate `test_data_slice.sql` with a small but internally consistent snippet
# of real data for testing
psql -f make_sample_db.sql codetalker
pg_dump -f test_data_slice.sql -n snippet codetalker
echo "DROP SCHEMA public CASCADE; ALTER SCHEMA snippet RENAME TO public" >> test_data_slice.sql
dropdb codetalker_test; createdb codetalker_test
psql -f test_data_slice.sql codetalker_test
dropdb codetalker_dev; createdb --template=codetalker_test codetalker_dev
