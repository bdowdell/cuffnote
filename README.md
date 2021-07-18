# cuffnote
A python library for simple mortgage calculations

## package modules

1. **cuffnote.mortgages.Mortgage**: The base class represents a plain vanilla mortgage
1. **cuffnote.mortgages.ExtraMonthlyPrincipal**: Inherits from the base class & allows modelling a mortgage with extra monthly principal payments. The start date of the extra payments does not have to be the same as the start date of the loan.

## running unittests using coverage & unittest

First, create a file called `.coveragerc` so coverage knows what source files to test:

```
[run]
source = cuffnote/
```

Launch the unittests using coverage:

`$ coverage run -m unittest -v tests/test_* ; coverage html`