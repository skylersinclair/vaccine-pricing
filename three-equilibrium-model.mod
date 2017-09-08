set Manufacturers ordered;

var publicPrice{m in Manufacturers} >=0;
var publicQuant{m in Manufacturers} >=0;
var privatePrice{m in Manufacturers} >=0;
var privateQuant{m in Manufacturers} >=0;
var privateCapacity{m in Manufacturers} >=0;
var privateQC{m in Manufacturers} >=0;
var compEquil{m in Manufacturers} binary;
var mixedEquil{m in Manufacturers} binary;
var bertEquil{m in Manufacturers} binary;
var qcNeg{m in Manufacturers} binary;
var k1Larger binary;

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
param N >=0;

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

# Calculate qC, setting it to zero if the qC formula gives a negative
subject to privateQCConstraint{m in Manufacturers, j in Manufacturers: m <> j}:
	privateQC[m] = 0.5 * (a_r[m] * (1 - gamma) - gamma * privateCapacity[j]) * (1 - qcNeg[m]);
# Enforces that if qC formula positive, that qcNeg = 0
subject to qCPositiveConstraint{m in Manufacturers, j in Manufacturers: m <> j}:
	0.5 * (a_r[m] * (1 - gamma) - gamma * privateCapacity[j]) <= N * (1 - qcNeg[m]);
# Enforces that if qC formula negative, that qcNeg = 1
subject to qCNegativeConstraint{m in Manufacturers, j in Manufacturers: m <> j}:
-0.5 * (a_r[m] * (1 - gamma) - gamma * privateCapacity[j]) <= N * qcNeg[m];

# --- STUFF WITH EQUILIBRIA ---

# Bertrand-Chamberlin Equilibrium
subject to bertrandCapacityConstraint{m in Manufacturers}:
	privateCapacity[m] >= k_gamma[m] - N * (1 - bertEquil[m]);
subject to bertrandPriceConstraint1{m in Manufacturers}:
	privatePrice[m] <= a_r[m] / (2 * b_r[m] - c_r[m]) + N * (1 - bertEquil[m]);
subject to bertrandPriceConstraint2{m in Manufacturers}:
	privatePrice[m] >= a_r[m] / (2 * b_r[m] - c_r[m]) - N * (1 - bertEquil[m]);
	
# Mixed Strategy Equilibrium (using the max value of the mixed strat)
subject to mixedCapacityConstraint1{m in Manufacturers}:
	privateCapacity[m] >= privateQC[m] - N * (1 - mixedEquil[m]);
subject to mixedCapacityConstraint2{m in Manufacturers}:
	privateCapacity[m] <= k_gamma[m] + N * (1 - mixedEquil[m]);
subject to mixedPriceConstraint1{m in Manufacturers}:
	privatePrice[m] <= 0.5 * (a_r[m] * (1 - gamma) - privateCapacity[last(Manufacturers)] * gamma) * k1Larger + 0.5 * (a_r[m] * (1 - gamma) - privateCapacity[first(Manufacturers)] * gamma) * (1-k1Larger) + N * (1 - mixedEquil[m]);
subject to mixedPriceConstraint2{m in Manufacturers}:
	privatePrice[m] >= 0.5 * (a_r[m] * (1 - gamma) - privateCapacity[last(Manufacturers)] * gamma) * k1Larger + 0.5 * (a_r[m] * (1 - gamma) - privateCapacity[first(Manufacturers)] * gamma) * (1-k1Larger) - N * (1 - mixedEquil[m]);
# guarantee that if k1 larger, k1Larger = 1
subject to k1LargerConstraint:
	privateCapacity[first(Manufacturers)] - privateCapacity[last(Manufacturers)] <= N * k1Larger;
# guarantee that if k2 larger, k1Larger = 0
subject to k1SmallerConstraint:
	privateCapacity[last(Manufacturers)] - privateCapacity[first(Manufacturers)] <= N * (1 - k1Larger);

# Competitive Equilibrium 
subject to compCapacityConstraint{m in Manufacturers}:
	privateCapacity[m] <= privateQC[m] + N * (1 - compEquil[m]);
subject to compPriceConstraint1{m in Manufacturers, j in Manufacturers: m <> j}:
	privatePrice[m] <= a_r[m] * gamma - privateCapacity[m] - gamma * privateCapacity[j] + N * (1 - compEquil[m]);
subject to compPriceConstraint2{m in Manufacturers, j in Manufacturers: m <> j}:
	privatePrice[m] >= a_r[m] * gamma - privateCapacity[m] - gamma * privateCapacity[j] - N * (1 - compEquil[m]);
	
# --- STEPWISE PRIVATE CALCULATIONS ---

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
	
# Only one equilibrium type should be satisfied at once
subject to equilibriumConstraint{m in Manufacturers}:
	compEquil[m] + mixedEquil[m] + bertEquil[m] = 1;