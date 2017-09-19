# Python Script to take vaccine data input and turn it into a data
# file for AMPL
# Dina Sinclair 3/27/17

import math

def make_data_file(manu1,
                   manu2,
                   demand1, # PUBLIC SECTOR demand, not demand over both sectors
                   demand2,
                   min_profit1,
                   min_profit2,
                   capacity1,
                   capacity2,
                   gamma,
                   demand_combined = True,
                   scaling=100000,
                   percent_public = 0.57,
                   T = 0.1):

    # Calculate the needed constants
    a_u1 = demand1 * 0.5 * scaling
    a_u2 = demand2 * 0.5 * scaling
    a_r1 = demand1 * (1/percent_public) * 0.5 * scaling
    a_r2 = demand2 * (1/percent_public) * 0.5 * scaling
    b = (1 / ((1 + gamma) * (1 - gamma))) * scaling
    c = (gamma / ((1 + gamma) * (1 - gamma))) * scaling

    # Demand is slightly more complicated, since you can have separate demands
    # reported or one demand for both vaccines reported collectively.
    if demand_combined:
        if demand1 != demand2:
            print("Error. Expecting demand1=demand2 if demand_combined=True")
        else:
            D = demand1
    else:
        D = demand1 + demand2 #could be max of both rather than sum?

    # Create a file to write to
    f = open('Data_files\{0}_{1}_gamma{2}.txt'.format(manu1,manu2,str(gamma)), 'w')
    print ('opened file')
    
    # Define set(s)
    f.write('set Manufacturers:= {0} {1};\n'.format(manu1, manu2))
    f.write('\n')
    
    # Define parameters that don't depend on the manufacturer
    f.write('param gamma:= {0};\n'.format(str(gamma)))
    f.write('param D:= {0};\n'.format(str(D)))
    f.write('param T:= {0};\n'.format(str(T)))
    f.write('param percentPublic:= {0};\n'.format(str(percent_public)))
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
    # Note: we only look at the private sector k(gamma), so the
    # a value we input here is going to be a_r = demand*(1/0.57)*scaling
    alpha = a*(1+gamma)
    #print (alpha)
    #print ((1-(2*math.sqrt(1-gamma))/((2-gamma)*math.sqrt(1+gamma)))*(1/gamma))
    return (alpha/gamma)*(1-(2*math.sqrt(1-gamma))/((2-gamma)*math.sqrt(1+gamma)))
            
            

if __name__ == "__main__":
        
    make_data_file('infanrix',
                   'tripedia',
                   demand1 = 2.3,
                   demand2 = 2.3,
                   min_profit1 = 49600000,
                   min_profit2 = 35200000,
                   capacity1 = 20000000,
                   capacity2 = 20000000,
                   gamma = 0.23,
                   demand_combined = True)

    make_data_file('engerixB',
                   'recombivaxHB',
                   demand1 = 5.1,
                   demand2 = 5.1,
                   min_profit1 = 49600000,
                   min_profit2 = 95200000,
                   capacity1 = 20000000,
                   capacity2 = 20000000,
                   gamma = 0.76,
                   demand_combined = True)

    make_data_file('pentacel',
                   'pediarix',
                   demand1 = 4.5,
                   demand2 = 1.5,
                   min_profit1 = 35200000,
                   min_profit2 = 49600000,
                   capacity1 = 20000000,
                   capacity2 = 20000000,
                   gamma = 0.18,
                   demand_combined = False)
