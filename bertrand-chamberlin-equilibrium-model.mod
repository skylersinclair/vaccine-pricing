set Manufacturers;

var publicPrice{m in Manufacturers} >=0;
var publicQuant{m in Manufacturers} >=0;
var privatePrice{m in Manufacturers} >=0;
var privateQuant{m in Manufacturers} >=0;
var privateCapacity{m in Manufacturers} >=0;

param a_u{m in Manufacturers} >=0;
param b_u{m in Manufacturers} >=0;
param c_u{m in Manufacturers} >=0;
param a_r{m in Manufacturers} >=0;
param b_r{m in Manufacturers} >=0;
param c_r{m in Manufacturers} >=0;

param K{m in Manufacturers} >=0;
param P{m in Manufacturers} >=0;
param k_gamma{m in Manufacturers} >=0;

param gamma >=0;
param D >=0;

# --- OBJECTIVE FUNCTION ---

minimize cost:
	sum{m in Manufacturers}(publicPrice[m]*publicQuant[m]);
	
# --- STEPWISE PUBLIC CALCULATIONS ---

# Public quantities follow public linear demand curve	
subject to publicQuantConstraint{m in Manufacturers, j in Manufacturers: m <> j}:
	publicQuant[m] = a_u[m] - b_u[m] * publicPrice[m] + c_u[m] * publicPrice[j];

# Calculate private capacity 
subject to privateCapConstraint{m in Manufacturers}:
	privateCapacity[m] = K[m] - publicQuant[m];

# --- PRIVATE EQUILIBRIUM CALCULATIONS ---

# Ensure in Bertrand-Chamberlin Equilibrium region
subject to equilibriumMinConstraint{m in Manufacturers}:
	privateCapacity[m] >= k_gamma[m];

# Calculate Bertrand-Chamberlin optimal price
subject to privatePriceConstraint{m in Manufacturers}:
	privatePrice[m] = a_r[m] / (2 * b_r[m] - c_r[m]);

# Determine private quant according to private linear demand curve	
subject to privateQuantConstraint{m in Manufacturers, j in Manufacturers: m <> j}:
	privateQuant[m] = a_r[m] - b_r[m] * privatePrice[m] + c_r[m] * privatePrice[j];
	
# --- ADDITIONAL CONSTRAINTS ---

# Ensure total demand is met
subject to totalDemandConstraint:
	sum{m in Manufacturers}(publicQuant[m] + privateQuant[m]) >= D;
	
# Ensure manufacturers make at least min profit P	
subject to priceThresholdConstraint{m in Manufacturers}:
	publicQuant[m] * publicPrice[m] + privateQuant[m] * privatePrice[m] >= P[m];