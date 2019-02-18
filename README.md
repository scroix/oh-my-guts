![example_oh-my-guts](https://user-images.githubusercontent.com/9277107/52920689-97055a00-3363-11e9-8f87-de51cdc5ef8a.gif)

# oh-my-guts
Variation of now defunct 'oh-my-cv' people tracker, now turned capacitive sensing supervisor included in the up-coming exhibition from Museums Victoria, Gut Feelings. 

## Setup
`pip install -r requirements.txt`

## Run
`python oh-my-guts.py`

## Guide
Starts to read serial data from the first available USB Serial Device.

Is expecting a stream of Strings representing the state of the sensors, 0=Off, 1=On.

11100
00011
01001
11100

The socket server is accessible on 6789.

In addition there is a Flask server launched on start-up on port 5000 indicating sensor status.

A subscription to the websocket will provide updates on state changes in the following JSON form.

``` json
{
  "state": [
    false,
    true,
    false,
    false,
    true
  ],
  "count": 2
}
```
