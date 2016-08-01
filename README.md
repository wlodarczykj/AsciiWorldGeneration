# AsciiWorldGeneration
A Python implementation to randomly generate worlds much like Dwarf Fortress.

##Land
###Algorithm
The algorithm used is to leverage a perlin noise function. The code takes a point and plugs it into the Perlin Noise function.
Then the code scores the point based on the distance from each edge, and the output of the noise function.
The further from an edge and the larger the value of the noise function output will yield a land point.
If the score falls below a certain acceptance criteria it will be rejected and kept as ocean.

The code currently produces something like the following:
###Examples
![Example](result.bmp)

##Rivers
###Algorithm
First the algorithm finds a random point of land closest to the ocean.
After finding this point it finds an end point, which currently is simply another point
closest to the ocean on the same island. Then it will run A* to find the path from
one point to the next one.

Then, it takes this path generated and runs a Midpoint Displacement algorithm to
introduce some randomness.
###Examples
![Example](Examples/Rivers/river.bmp)
