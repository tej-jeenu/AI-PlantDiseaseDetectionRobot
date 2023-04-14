# PlantProject
Intention Behind my Project
The aim of this project was to understand how to implement deep learning in a project whilst attempting to 
Tackle a real world problem. I was looking into Object Detection through the YOLO algorithm to identify different types of plants including diseased and Healthy.  
The inspiration behind this was the awareness of lots of money being lost through farming simply through lack of awareness of plants having diseases, 
Furthermore for a lot of people it is the only means of survival and so undiscovered plant disease can eliminate basic human needs for some people, 
I therefore realised that it is a significant problem and was curious to investigate it. If there was a way to detect the diseases in plants early and 
inform specific treatments to those identified diseases as well the problem would be reduced.

What my project does?
	- The idea of my project is to simulate a AI drone
	- The Drone which in my case is an Arduino Car Robot will move in small distance increments
	- For each increment the Car moves, it will use the camera to view the surroundings or plants beneath in the case of the drone
	- The image data will be analysed from a computer with my AI model to identify the plant (healthy or diseased)
	- For each increment moved a map will be generated as a text file and each cell in the line of the file will represent every increment the Bot has moved across the field.
	- The cell will be written X if a disease is present in the cell or - if there is no disease present
	- A general map is also made to specify the plants detected at each increment the bot moves
	- The idea is that the disease map and general map can be viewed alongside eachother to see what diseases there are and their location.
	- In reality, geotagging would be a better idea and then a map would look at the geotagged properties of each image and form a compiled image of the detected plants and diseases in a field 
	- Furthermore, I used a relationaldatabase to specifiy what treatments to apply based on what plants were detected.
	- Another reason for the database is to notify specific farmers to apply treatments 
	- To control which farmers are sent which kinds to treatments to do, I made the option to add the farmers details to a database including their name, phone number for notifying and job key words
	- These key words are used to determine if a farmer is responsible for a specific treatment.
	- These farmers are notified automatically through whatsapp as soon as a field is scanned.
	- I made the treatments so that they can be repeated at intervals in case the treatment had to applied more than once therefore I specified date and repeat attributes in my database tables to determine when the treatment has to be applied again through SQL operations e.g. Adding the interval days to the date that the treatment was notified that day for reminding again
	- Overall this can ensure farmers can do the treatments as soon as possible as they have gained awareness, it is also very efficient as it avoids the human effort of having to decide who does what task as it is done automatically

What I used:
	- C# for UI
	- Python for mainprocessing e.g. Model, data processing, SQL
	- PostGreSQL for relational database
