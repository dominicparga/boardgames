# Boardgames

This little repo serves as handy tool to get information in boardgames through calculation or simulation.

## Boardgame: Risk

### Usage

```zsh
# for testing
py -m tests.risk

# for simulating
py -m risk --logging-level info --force-output

# for postprocessing
py -m postprocessing --input ./build/risk.json
```

> Note:
>
> `py -m unittest test.risk`
>
> is executing the module unittest giving test.risk as parameter, while
>
> `py -m test.risk`
>
> executes test.risk, which calles `unittest.main()`

### Results

What is the percentage that 1-3 attackers defeat a defence of 1-2 defenders?

In the following table

- `defended` means, that the attacker has lost all of its units.
- `draw` means, that the attacker and defender have lost one unit each.
- `defeated` means, that the defender has lost all of its units.

Example: To get the result for 2 attackers vs. 1 defender, you have to look at the row `2> (1`.

| winner (%) |   defenders   |    both     |   attackers   |
|:----------:|--------------:|------------:|--------------:|
|  `1>` `(1` |     (*) 58    |         0   |         42    |
|  `1>` `(2` |     (*) 75    |         0   |         25    |
|  `2>` `(1` |         43    |         0   |     (*) 57    |
|  `2>` `(2` |     (*) 45    |        32   |         23    |
|  `3>` `(1` |         35    |         0   |     (*) 65    |
|  `3>` `(2` |         29    |        34   |     (*) 37    |
