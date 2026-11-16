# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/budybozz/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/budybozz/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

4 KB deterministic chess engine for make.fun's "Build the strongest chess engine in 4 KB of Python" bounty.

## Run it

```sh
python3 main.py
```

Enter UCI commands: `uci`, `isready`, `position startpos`, `go`, `quit`.

## Engine Details

- 0x88 mailbox board representation
- Material-only evaluation (P=100, N=320, B=330, R=500, Q=900, K=20000)
- Alpha-beta search with iterative deepening
- Deterministic, no randomness, stdlib only

---

<sub>Entered on [make.fun](https://make.fun/?ref=budybozz&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>