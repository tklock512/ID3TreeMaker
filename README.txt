Author: Terrence Klock
This program was developed on Windows. 

To compile and run the program, navigate to the directory containing the program. Then, enter the command:

	python .\ID3TreeMaker.py train.dat test.dat

The train.dat and test.dat files should contain the training data and testing data respectively. BOTH MUST BE IN THE COMMAND LINE FOR THE PROGRAM TO RUN.

The learning curve is also present in this folder for a given train.dat and test.dat. The curve is logarithmic, and at a certain point new training data
fails to significantly improve the accuracy of the decision tree. This is to be mostly expected. 