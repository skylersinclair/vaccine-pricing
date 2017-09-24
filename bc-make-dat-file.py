# Python Script to take vaccine data input and turn it into a data
# file for AMPL bertrand-chamberlin equilibrium script
# Dina Sinclair 9/24/17

import math

def make_data_file(manu1,
                   manu2,
                   total_demand1,  
                   total_demand2,
                   min_profit1,
                   min_profit2,
                   capacity1,
                   capacity2,
                   gamma,
                   demand_combined = True,
                   scaling=100000,
                   percent_public = 0.57,
                   ):
    '''
    This file takes the input
     - Manufacturer strings manu1 and manu2 for file naming purposes.
     - Integers total_demand1 and total_demand2 that represent the total
       (across public and private sectors) demand for each manufacturer. If
       the total demand used represents the combined demand of both
       manufacturers, then enter that same number for both manufacturers and
       set demand_combined to True. If the demand for each manufacturer is
       distinct, enter each separate value as appropriate and set
       demand_combined = False.
     - Integers min_profit1 and min_profit2 indicate the values of minimum
       profit P desired for manufacturers 1 and 2 respectively.
     - Integers capacity1 and capacity2 indicate the capacity K of each of
       the two manufacturers.
     - Float gamma is the degree of product differentiation, from 0 to 1.
     - Boolean demand_combined is set to true if the total_demand value
       entered represents the demand of both manufacturs summed together
       rather than reporting each demand separately. When demand_combined
       is false, we assume that total demand is the sum of the two separate
       demands D = total_demand1 + total_demand2.
     - Integer scaling is used in b and c calculations and comes from the
       current method of calculating gamma using number of adverse effects.
     - Float public_percent is the percentage of vaccines sold in the
       public sector.
    '''

    # Calculate the needed constants
    public_demand1 = total_demand1 * percent_public
    public_demand2 = total_demand2 * percent_public
    a_u1 = public_demand1 * 0.5 # a_u uses only public demand
    a_u2 = public_demand2 * 0.5
    a_r1 = total_demand1 * 0.5 # a_r uses total demand not private only
    a_r2 = total_demand2 * 0.5
    b = (1 / ((1 + gamma) * (1 - gamma))) * scaling 
    c = (gamma / ((1 + gamma) * (1 - gamma))) * scaling

    # Calculate D, total demand over the entire market
    # Note that this depends on if total demand is orginally combined for
    # both manufacturers or reported separately.
    if demand_combined:
        if total_demand1 != total_demand2:
            print("Error. Expecting demand1=demand2 if demand_combined=True")
        else:
            D = total_demand1
    else:
        D = (total_demand1 + total_demand2) 

    # Create a file to write to
    f = open('Generated_Data\{0}_{1}_gamma{2}.txt'.format(manu1,manu2,str(gamma)), 'w')
    print ('opened file')
    
    # Define set(s)
    f.write('set Manufacturers:= {0} {1};\n'.format(manu1, manu2))
    f.write('\n')
    
    # Define parameters that don't depend on the manufacturer
    f.write('param gamma:= {0};\n'.format(str(gamma)))
    f.write('param D:= {0};\n'.format(str(D)))
    f.write('\n')

    # Define parameters that do depnd on the manufacturer
    f.write('param: P:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     str(min_profit1),
                                                     manu2,
                                                     str(min_profit2)))
    f.write('param: K:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     str(capacity1),
                                                     manu2,
                                                     str(capacity2)))
    f.write('param: k_gamma:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % k_gamma(gamma,a_r1)),
                                                     manu2,
                                                     '%s' % float('%.3g' % k_gamma(gamma,a_r2))))
    f.write('param: a_u:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % a_u1),
                                                     manu2,
                                                     '%s' % float('%.3g' % a_u2)))
    f.write('param: b_u:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % b),
                                                     manu2,
                                                     '%s' % float('%.3g' % b)))
    f.write('param: c_u:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % c),
                                                     manu2,
                                                     '%s' % float('%.3g' % c)))
    f.write('param: a_r:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % a_r1),
                                                     manu2,
                                                     '%s' % float('%.3g' % a_r2)))
    f.write('param: b_r:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % b),
                                                     manu2,
                                                     '%s' % float('%.3g' % b)))
    f.write('param: c_r:=\n{0}  {1}\n{2}  {3};\n\n'.format(manu1,
                                                     '%s' % float('%.3g' % c),
                                                     manu2,
                                                     '%s' % float('%.3g' % c)))
    f.close()

    
def k_gamma(gamma, a):
    ''' Calculates k_gamma from floats gamma (product diff) and
        a (demand curve constant). Since we are assuming the public sector
        buys vaccines first, we will be using a_r to calculate k_gamma and
        ensure that k_r >= k_gamma.
    '''
    alpha = a*(1+gamma)
    return (alpha/gamma)*(1-(2*math.sqrt(1-gamma))/((2-gamma)*math.sqrt(1+gamma)))
            
            
if __name__ == "__main__":
    # This example mimics figure 5.1 and dat file
    # bc-equilibrium-model-P-variation.dat with minor rounding differences
    make_data_file('infanrix',
                   'daptacel',
                   total_demand1 = 4000000,
                   total_demand2 = 4000000,
                   min_profit1 = 0,
                   min_profit2 = 0,
                   capacity1 = 4000000,
                   capacity2 = 4000000,
                   gamma = 0.23,
                   demand_combined = True)

    # This example mimics figure 5.2 and dat file
    # bc-equilibrium-model-gamma-variation.dat with minor rounding differences
    make_data_file('infanrix',
                   'daptacel',
                   total_demand1 = 4000000,
                   total_demand2 = 4000000,
                   min_profit1 = 15200000,
                   min_profit2 = 15200000,
                   capacity1 = 4000000,
                   capacity2 = 4000000,
                   gamma = 0,
                   demand_combined = True)
