## TASK

- [ ] Add connection with db
    - [x] Create sqlite database
    - [x] Create table to store users
    - [x] Add methods to comunicate with database
    - [ ] Create table to store inspections record id
- [ ] Users and Navigation
    - [x] Store User in db
    - [x] Hash password
    - [x] Create a middleware to handle request and verify token
    - [ ] Verify token in each navigation action
- [ ] Data management
    - [ ] Send list of available inspections
    - [ ] StripChart
        - [x] Read json StripChart 
        - [x] Retrieve StripChart data
    - [ ] Pie Chart
        - [ ] Calculate statistics from selected inspections
        - [ ] Create endpoint to handle pie chart requests