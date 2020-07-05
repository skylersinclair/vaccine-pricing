## Vaccine Pricing Models in AMPL

Dina Sinclair 5/31/17

This is the code needed to reproduce figures 5.1 and 5.2 of the research project [Incorporating the Centers for Disease Control and Prevention into Vaccine Pricing Models](https://scholarship.claremont.edu/hmc_theses/111/) that makes use of quadratic programming and game theory to better understand pricing in vaccine dupoplies.

The .mod files are the two models (bertrand-chamberlin and three-
equilibrium). Only the bertrand-chamberlin model is currently
functional. The .dat files are the data used for the P variation
(figure 5.1) and gamma variation (figure 5.2). To run these, you
need AMPL scripts P-variation.txt and gamma-variation.txt 
respectively. Make sure that the .dat and .mod files are in your
AMPL folder, open the AMPL commmand line, and copy and paste
the desired script into to the prompt line. The code will then
run and create a .txt output under the name test_output.txt.
This output can be read by excel as an input comma-separated
csv file to make plots.
