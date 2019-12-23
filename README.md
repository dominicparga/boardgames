# Boardgames

This little repo serves as handy tool to get information in boardgames through calculation or simulation.

## Usage

Just run the script `./scripts/run.sh`, which first executes python-tests before running the `risk`-module.

## Results

In the following, all results are presented.

### Risk

What is the percentage that 1-3 attackers defeat a defence of 1-2 defenders?

In the following table

- `defended` means, that the attacker has lost all of its units.
- `draw` means, that the attacker and defender have lost one unit each.
- `defeated` means, that the defender has lost all of its units.

Example: To get the result for 2 attackers vs. 2 defenders, you have to look at the row `d=2` under `a=2`.

|  %  | defended |  draw | defeated |
|:---:|:--------:|:-----:|:--------:|
|     |          |  a=1  |          |
| d=1 |   ??.??  | ??.?? |   ??.??  |
| d=2 |   ??.??  | ??.?? |   ??.??  |
|     |          |       |          |
|     |          |  a=2  |          |
| d=1 |   ??.??  | ??.?? |   ??.??  |
| d=2 |   ??.??  | ??.?? |   ??.??  |
|     |          |       |          |
|     |          |  a=3  |          |
| d=1 |   ??.??  | ??.?? |   ??.??  |
| d=2 |   ??.??  | ??.?? |   ??.??  |
