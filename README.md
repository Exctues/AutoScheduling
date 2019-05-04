# Automatic Time Table creation  
Purpose of the project - create web-service which enable DOE to  
create appropriate university schedule based on imported data.  

## Current features of the project:
1. User profiles (login/logout/register)
2. Upload files and see history of uploaded files
3. Generate schedule and see history of generated schedule & edit pr. schedules
4. Visualisation on site & google spreadsheet

## Core of the system - scheduling
Good research on scheduing: [Scheduling using genetic algorithm](https://www.codeproject.com/Articles/23111/Making-a-Class-Schedule-Using-a-Genetic-Algorithm)  
As a base for our scheduler, we use a Genetic algorithm.  
How it works:    
* An initial population is generated based on imported data;  size of population - 100 
* Fitness function of the prototype is based on a number of intersections between groups, auditoriums, 
 and faculties / order of lesssons & size of auditoriums & groups
* Crossover swaps day, time and auditorium of mating schedules (chromosomes);  
* Mutation function randomly changes a day, time and auditorium;  
* Repeat till ideal fitness is reached or 30 000 generations will run;  
* Export schedule somewhere  


## Technology Stack
* Python3
* Django
* C++ 11
* Bootstrap/JQuery
* Gsript

# Running project
## Preparing server for running C++ schedule
1. Clone this repository to your machine;
2. Install MinGW (Windows) and CMake if needed;
3. Clone submodules with:
    * git submodule sync
    * git submodule init
    * git submodule update
4. Create folder scheduler_cpp/files
5. Run the server.

**Here are additional notes for different Operating Systems.**
### Windows
Specify path to MinGW bin folder and CMake in variable PATH.
The PATH should contain only one copy of MinGW so that everything worked fine.

### Linux
Installing CMake should be enough.

## How to run the server 
1. `pip3 install -r requirements.txt`  
2. `cd site`
3. `python manage.py makemigrations && python manage.py migrate`
2. `python3 manage.py runserver`
