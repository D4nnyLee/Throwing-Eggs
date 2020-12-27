# Throwing Eggs

## Introduction

This is a django-based line bot that provide a little game to play.

### Scenario

Now you have 3 eggs, I want to know the
**MAX** number `X` such that the egg won't break
if I throw it from Xth floor of the building.

The range for `X` is 0 ~ 1000.

Note that if the egg is not broken,
it will be thrown *again* in the next trial.

Please help me to find the number X within at most 30 trials.

### Usage

Different input has different function.

* `#` : Get the information of remain throwing times and eggs.
* `? N` : Query the result of throwing egg from Nth floor.
* `! N` : Check whether N is the answer or not and restart game.

## FSM diagram

![](https://i.imgur.com/uv7XFTc.png)

## Reference

1. [Django documentation](https://docs.djangoproject.com/en/3.1/)
2. [Line Message API reference](https://developers.line.biz/en/reference/messaging-api)
