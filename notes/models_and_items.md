# Understanding the flow of data models and json schemas in an API

- API's have a specific purpose to manipulate data programmatically, each backend system is different somehow but consist of the same principals, some follow REST architecture or others (like GraphQL maybe) 
- After using Django, FASTapi and Flask the common pattern after the request hits the server is to fetch the data from the database, the data then will be handled by the controller then parsing it in into json or xml then finshing up with sending a response or an error.

    - Request
    - Data 
    - Processing
    - Parsing 
    - Response 

- All of these steps are handled by different libraries like pydantic for serealizing, sqlalchemy for data modeling and each framework has it's alternative 