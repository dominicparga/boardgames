#!/usr/bin/env sh

# Note:
#
# python -m unittest test.risk
# is executing the module unittest giving test.risk as parameter, while
#
# python -m test.risk
# executes test.risk, which calles unittest.main()

clear
if python -m tests.risk; then
    clear
    python -m risk --max-fight-rounds 10_000 --log info "${@}"
else
    # script-return-value should be false if test is false
    false
fi
