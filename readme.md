# ACVL Utilities

This repository contains functions / algorithms that the ACVL group uses frequently. Thus, we created this repository to have a central place with efficient implementations of these functions / algorithms.

## How to contribute
1. Create a new branch following this convention:
   - To add a new feature: feature_"feature name" (e.g. feature_padding)
   - To fix a bug in an existing feature: bugfix_"bug name" (e.g. bugfix_)
   - To improve an existing feature: improv_"feature name" (e.g. improv_sampler)
2. Commit your changes
3. Create a pull request
   - Assign at least one reviewer to the pull request. Do not always assign Fabian!

## How to review a pull request
- Check the feature documentation
  - Is it understandable?
  - Does it cover the entire feature?
  - Is it grammatically correct?
- Check the code
  - Is the code understandable?
  - Would you implement it similarly?
  - Is it more or less well-structured?
  - Is it split into multiple methods if or just one big blob?
  - Are function and variable names intuitive?
  - Check for expensive operations
  - What not to do:
    - Don't check every single line
    - Don't check every single line for correctness
- Check the tests
  - Do all tests run?
  - Are most feature cases covered?


## How to merge
- Please check both boxes: `squash commits` AND `delete source branch`. Otherwise we will accumulate a million branches over time


## Packages

### Array manipulation

#### Slicer:
A dynamic N-dimensional array slicer that returns a tuple that can be used for slicing an N-dimensional array. Works exactly as Python and Numpy slicing, only with different syntax.
The conventional slicing method has the drawback that one must know the dimensionality of the array beforehand. By contrast, this slicer can be adapted dynamically at runtime.


### Miscellaneous

#### Imap tqdm:
Run a function in parallel with a tqdm progress bar and an arbitrary number of arguments.
Results are always ordered and the performance should be the same as of Pool.map.
