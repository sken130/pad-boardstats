# pad-boardstats

This is a library which simplifies the process of simulating boards and
checking for how often conditions are met.

For example, you might want to see how often you get a fire, water, wood match
in a natural board. 

```python
config = standard_config(minimum_counts={'r': 3, 'b': 3, 'g': 3})
run_test(config)
```

Maybe you want to see how often you get at least 10 green orbs and 10 red orbs
in a tricolor.

```python
config = standard_config(
    natural=False,
    orb_types=['r', 'b', 'g'],
    minimum_counts={'r': 10, 'g': 10})
run_test(config)
```

### Getting Started

For a quick start, check out `sim.py` which is the main driver, and `tests.py`
for some example configurations.

Take a look at `config.py` for more details about how to set up a
configuration. The `Config` object has some helpers that make setting it up
easy for common use cases, and if you need more complex use cases, you can create
your own `Validator` objects.

Support is available for match-N leads (defaults to 3) and alternate board
sizes (defaults to 6x5).

There are some unit tests in `validation.py`.

### Note about board generation

There is some discussion over the method PAD uses to generate boards,
specifically regarding the 'minimum orb count'. It's a fact that every board
change in PAD spawns at least 3 orbs of each color. 

The two options are:
1) Generate a board, and then check if it is valid (3 orbs of each spawn)
color. If not valid, regenerate until valid.
2) Fix 3 orbs of each spawn color in the board, then randomly pick every
other orb color.

The first option results in a fatter tail distribution, the second a thinner
one. E.g. with option 2, a bicolor will be significantly less likely to
generate 3-4 orbs than with option 1. See the outputs below for another
practical example.

Some experimental testing by Shmifty on Discord points to the second option, so
that is the default setting. To change this setting, adjust the value of
`FORCE_FIXED_REQUIRED_ORBS` in `config.py`.

### Sample output

Here are the outputs for Reiwa:

```
reiwa 5x6 natural board
Done: 15704 success 34296 fail, 31.41%

With FORCE_FIXED_REQUIRED_ORBS = False:

reiwa 5x6 5-color
Done: 32914 success 17086 fail, 65.83%

reiwa 5x6 ygf (exact reiwa colors)
Done: 44387 success 5613 fail, 88.77%

With FORCE_FIXED_REQUIRED_ORBS = True:

reiwa 5x6 5-color
Done: 43137 success 6863 fail, 86.27%

reiwa 5x6 ygf (exact reiwa colors)
Done: 48903 success 1097 fail, 97.81%
```
