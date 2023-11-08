Release History
===============

## 0.1.7 (2023-11-08)
------------------

- Fixes for Python 3.7+.


0.1.6 (2023-03-05)
------------------

- Fix for rename sequences, indexes, constraints and M2M tables.


0.1.5 (2022-11-19)
------------------

- Fix NameError.


0.1.4 (2022-11-17)
------------------

- Fix for DB tables with uppercase chars.
- Get content_type name from the database instead of making assumption.


0.1.3 (2021-03-29)
------------------

- Handle table name truncation as Django does.


0.1.2 (2020-06-02)
------------------

- When ran multiple times at the same time, Exception would raise from rename queries. Catch and log this instead of crashing.


0.1.1 (2020-06-01)
------------------

- Documentation updates.


0.1.0 (2020-06-01)
------------------

-   Initial release.
