# JSON Flask Pandas Micro-Service
A short assessment piece.
## The Task
Create an API for an HR system that returns JSON.  

An example JSON file is attached in this repository.

Use Flask to build the API. Can use any database of choice for holding the data.
## The Data 
Following data set will be provided as an array of objects: 

Unique Identifier - First Name - Last Name - DOB - Industry - Annual income - other fields
## Expected behaviour
The API should support the following operations on the included dataset: 
- Read all (sorting, pagination, filtering provided as parameters). 
- Read one. 
- Update one. 
- Delete one. 

The API should also be able to return the following statistics on a set of different endpoints from the above (Pandas implementation): 
- Average age per industry 
- Average salaries per industry.
- Average salaries per years of experience.
- Based on the dataset, other “interesting” statistics.

Basic validation should be in place for the above operations where required .
