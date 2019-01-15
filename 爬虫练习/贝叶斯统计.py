def BayesianCount(a,b):
    if b != 0:
        s = a + b
        return (a/s)*(1/2)/(b/s)
    else:
        return 0.5




print(BayesianCount(1,1));
print(BayesianCount(18,3));
print(BayesianCount(14,1));
print(BayesianCount(16,0));
print(BayesianCount(5,18));
print(BayesianCount(72,17));
print(BayesianCount(120,20));
print(BayesianCount(1200,200));
print(BayesianCount(37,14));
print(BayesianCount(57,5));
