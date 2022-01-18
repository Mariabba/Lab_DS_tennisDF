# How to execute the pipeline
We have a pipeline of **4 python files**. The data has to be put into `data/inputs/`. All the data is in there already, except for `tennis.csv`, for space reasons. Requirements, in the form of libraries, are listed in `requirements.txt`.

So to execute the pipeline, you must:

1. Add `tennis.csv` into `data/inputs/`;
2. In the terminal: `pip3 install -r requirements.txt` to install the required libraries;
3. To execute the actual project: `python3 preprocessing.py` (or `python`,depending on your configuration);
4. `python3 divide.py`;
5. `python3 postprocessing.py`;
6. `python3 load.py`.


# Visual queries Readme
If you want to visualize again the results of the workflows, in the 'Destination File Flat' box you have to modify the file path and insert where to save it. This goes for all three Assignments.