# EtherPad-Collaboration-Analizer
This repository is meant for software made to add on to the code realized for the experiments in the
paper "Spacetime Characterization of Real-Time Collaborative Editing" (Gabriele D'Angelo, Angelo Di Iorio, Stefano~Zacchiroli).

For now, it only consists in a python 3 script that analizes a pad file and extracts a data structure which represents the textual distance of each action (i.e. insert, delete, update) from the closest text that another author wrote beforehand.


# To-do list
As of now, even if the script seems to be working correctly, I would still like to make plenty of QOL changes:
1) Make it so the file to be parsed is passed as an argument to the script
2) Add comments and more debug code where necessary
3) Test the file even more
