# AsciiWorldGeneration
A Python implementation to randomly generate worlds much like Dwarf Fortress.

##Algorithm

The algorithm to generate landmass is similar to a disease spreading algorithm.
The first step is to place a center randomly on the map with a specified score (currently).
The algorithm then iterates on the squares around the center. This next iteration will assign scores to these squares. 
The adjacent squares will either inherit the score from the center, or it will possibly inherit the (score - 1). Whether is inherits the score or the (score - 1) is determined based on a hard-coded (currently) probability.

##Example
The code currently produces something like the following:
![Example](result.bmp)
