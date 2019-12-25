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

#### Winning chance

In the following table, winning means that all opposite units have been destroyed.

Example: To get the winning-chance for 2 attackers vs. 1 defender, you have to look at the row `2> (1`.

| winner (%) |   defenders   |    both     |   attackers   |
|:----------:|--------------:|------------:|--------------:|
|  `1>` `(1` |     (*) 58    |         0   |         42    |
|  `1>` `(2` |     (*) 75    |         0   |         25    |
|  `2>` `(1` |         43    |         0   |     (*) 57    |
|  `2>` `(2` |     (*) 45    |        32   |         23    |
|  `3>` `(1` |         35    |         0   |     (*) 65    |
|  `3>` `(2` |         29    |        34   |     (*) 37    |

#### Chance of losing at least 1 unit

`(*)` means this team has the highest chance of winning the fight (see previous table).

| losing >= 1 unit (%) |   defenders   |   attackers   |
|:--------------------:|--------------:|--------------:|
|      `1>` `(1`       |   (*) 42      |       58      |
|      `1>` `(2`       |   (*) 25      |       75      |
|      `2>` `(1`       |       57      |   (*) 43      |
|      `2>` `(2`       |   (*) 55      |       77      |
|      `3>` `(1`       |       65      |   (*) 35      |
|      `3>` `(2`       |       71      |   (*) 63      |