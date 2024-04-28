# setup connection
def connection():
    import pyodbc
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=EPBYMINW02AF\\SQLEXPRESS01;DATABASE=TRN;UID=TestUser;PWD=1234')
    return conn


# TC №1. Check that table "Jobs" has 4 columns
# Expected result: 4 (four columns)
def test_check_number_columns():
    cursor = connection().cursor()
    cursor.execute("select count(distinct column_name) from INFORMATION_SCHEMA.COLUMNS where table_name = 'Jobs'")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] == 4


# TC №2. Check that table "Jobs" has record where job_title is 'Programmer'
# Expected result: 1 (one distinct row with job_title = 'Programmer')
def test_check_record_presence():
    cursor = connection().cursor()
    cursor.execute("select count(distinct job_title) from hr.jobs where job_title = 'Programmer'")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] == 1


# TC №3. Check that table "Locations" has column 'postal_code'
# Expected result: 1 (one column 'postal_code')
def test_check_column_presence():
    cursor = connection().cursor()
    cursor.execute("select count(distinct column_name) from INFORMATION_SCHEMA.COLUMNS where table_name = 'Locations' and Column_name = 'postal_code'")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] == 1


# TC №4. Check that table "Locations" doesn't contain duplicates by field "street_address"
# Expected result: 0 (no duplicates)
def test_check_no_duplicates_in_column():
    cursor = connection().cursor()
    cursor.execute("select count(*) from (select street_address from hr.locations group by street_address having count(*) > 1) as subquery")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] == 0


# TC №5. Calculate and check that max(salary) from "Employees" table is greater than 0
# Expected result: > 0 (max salary should be greater than zero)
def test_agg_functions_for_column():
    cursor = connection().cursor()
    cursor.execute("select round(max(salary),2) from hr.employees")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] > 0


# TC №6. Check that column "Email" doesn't contain NULLs in "Employees" table
# Expected result: 0 (no NULLS)
def test_check_no_nulls_in_column():
    cursor = connection().cursor()
    cursor.execute("select count(*) from hr.employees where email is null")
    rows = cursor.fetchone()
    connection().close()
    assert rows[0] == 0
