# COVID-19 Simulation Environment (Probability, Randomness, Visualisation and the SIR Model) 

A python application which simulates a pandemic by using real demographics (of India) and assumed probabilities based on health data to track infections. With built-in "filters" it is able to show how the SIR curves flatten if safety measures are applied (masks, gloves, lockdowns). It outputs two visualizations:

1. "People" moving around in a "world" (color coded according to whether they are infected, dead or susceptible)
2. SIR graph showing real-time rates 

* View a [demo](https://youtu.be/Htg_9UphC6Q) submitted to CS50 *

## Factors and Probability 

The simulation calculates recovery and infection using the following factors:

* Age
* Immuno-compromised Risk
* Chance of death
* Duration of infection or expected time to fatality
* Minimum distance for infection
* Probability of infection
* Indirect Information (touch, objects)
* Movement of people and the distance they travel
* Asymptomatic chance

These factors are not standalone, rather their proabilities continuously intersect each other for every person in the simulation. For example, an elderly person will more likely be immuno-compromised and time to fatality will be lesser. Or someone who is immuno-compromised might move around lesser than a healthy person. Or the chance of being asymptomatic can vary with age and health status. 

Along with these factors there are also safety measures that can be turned on and off by the user:

1. Masks
2. Gloves
3. Social Distancing

Setting these to `1` reduces the probability of infection and fatalities while increasing other factors such as the minimum distance for infection. When social distancing is on, people are restricted to a certain radius and the visualisation is able to show containment zones. 

## The Simulation

The application builds a "world" of a given size and populates it with objects (people). The density is adjustable by users to mimic a particular location. Every person is given health characteristics according to the weighted demographics of India. 0.75% of the people carry the infection at time = 0

The simulation runs for a number of "days", wherein every day each person moves out of their home location, randomly travels within a radius and comes back at the end of the day. Wherever infected people go they leave behind spots of infection (an object, in the air, etc.) which vanish in half a day. The distance and randomness of movement is controlled by their age and health attributes. For example, an infant doesn't travel, a teen travels a bit more, a middle-aged person travels a lot and the elderly travel a lot lesser. An immuno-compromised old person is even more restricted.

The interaction of the people with each other and the infected spots, weighted by their risk factors confirms whether they get the disease or not. If they do, we keep them infected for the standard 14 days multiplied by various health probabilities. Similarly we decide if some one dies or not depending on a random severity of the infection w.r.t to risk factors. 

The infected turn red and move a bit lesser while the dead turn black and are removed from the model. Some people are aysmptomatic and move around freely. Those who recover succesfully turn green.

## Results
 
The results of a few test runs and screenshots of the SIR model is saved in `Tests` directory. `SIR_restricted` shows how a curve is flattened when all safety restrictions are implemented versurs the `SIR_unrestricted` where the pandemic is not contained.

## Requirements and Running the Code

> pip3 install -r requirements.txt

* Run `simulation.py` to see the simulation environment. 
* To see the SIR visualization simultaneously, run `visualize_SIR.py` in a new terminal. 
* `simulation.py` saves all test data to `data.txt` in real time and appends to `afterData.csv` with final results. It also outputs the final result to the terminal.

## Acknowledgements

This application was motivated by a project assigned to me as a student of the Introduction to Computer Programming course at Ashoka Univerity, taught by Professor Debayan Gupta.
