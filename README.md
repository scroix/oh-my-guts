![example_oh-my-guts](https://user-images.githubusercontent.com/9277107/52920689-97055a00-3363-11e9-8f87-de51cdc5ef8a.gif)

# oh-my-guts
Variation of now defunct 'oh-my-cv' people tracker, now turned capacitive sensing supervisor included in the up-coming exhibition from Museums Victoria, Gut Feelings. 

## Setup
`pip install -r requirements.txt`

## Run
`python oh-my-guts.py`

## Guide
The socket server is accessible by default on 6789 and is configurable by `config.json`.

In addition there is a Flask server launched on start-up on port 5000 (unconfigurable) indicating sensor status.

A subscription to the websocket will provide updates on state changes in the following JSON form.

``` json
{
  "type": "state",
  "state": [
    true,
    true,
    true,
    false,
    false
  ],
  "count": 3
}
```
