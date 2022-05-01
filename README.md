## Task requirements:
`Goal`: The client is a reseller of running shoes (brand “*Fast Feed*”) and asked you to provide him insights about people that do running as a sport either professional or as a hobby. 

He would like to know how many people from
age 0-20, 21-30, 31-40, 41-50, 51+ are participating in the Zurich Marathon from 2014 – 2018. He is trying to do some research on the https://datasport.com/de/ but doesn’t know how to get the data:

### Task a. 

Write a webscraper in Python and parse the data from the Zurich Marathon from the website: https://services.datasport.com/2014/lauf/zuerich/alfab.htm for all athletes from the alphabet a-z,
from the year 2014 – 2018. The logic of the URL is as follows:

https://services.datasport.com/{year}/lauf/zuerich/alfa{x}.htm

where {`year`} is the year and {`x`} is the starting letter of the runner surname.

### Task b.

Store the data in a database with the following fields:
1. `Id` is an auto-generated integer (autoincrement)
2. `Category`: Varchar
3. `Rang`: varchar
4. `Fullname`: varchar
5. `Age_year`: integer
6. `Location`: varchar
7. `total_time`: timestamp
8. `run_link`: varchar
9. `run_year`: integer