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

This library assumes boards are generated randomly, and then checked for
validity; if invalid, a new board is generated. The alternative is to 'fix' 3
orbs of each color and then randomly generate the rest of the orbs. Comparison
of the two methods shows that you are more likely to get lower orb counts using
this library; e.g. with a bicolor you are more likely to get a 3/27 split. This
seems to fit my experience.


### Sample output

Here is the output from the 'default' tests included:

```
standard, should be 100%
Done: 50000 success 0 fail, 100.00%

Require 3 fire, natural board
Done: 45659 success 4341 fail, 91.32%

Require 4 fire, natural board
Done: 39139 success 10861 fail, 78.28%

Require 4 fire, orb change
Done: 40499 success 9501 fail, 81.00%

Require 3 fire 3 heart, natural board
Done: 41739 success 8261 fail, 83.48%

Require 4 fire 4 heart, natural board
Done: 29909 success 20091 fail, 59.82%

Require 4 fire 4 heart, orb change
Done: 31941 success 18059 fail, 63.88%

reiwa 5x6 natural board
Done: 15704 success 34296 fail, 31.41%

reiwa 5x6 5-color
Done: 32914 success 17086 fail, 65.83%

reiwa 5x6 ygf (exact reiwa colors)
Done: 44387 success 5613 fail, 88.77%

reiwa 6x7 natural board
Done: 40430 success 9570 fail, 80.86%

reiwa 6x7 5-color
Done: 47000 success 3000 fail, 94.00%

reiwa 6x7 ygf (exact reiwa colors)
Done: 49541 success 459 fail, 99.08%
```
