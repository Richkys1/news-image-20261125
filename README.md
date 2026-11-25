# The World Today — Wednesday, 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Richkys1/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Richkys1/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One front-page image summing up the world's news of Wednesday, 25 November
2026, built by an AI agent for make.fun's "Sum up 25 November's world news
in one image" bounty ($100 in USDC). Every story was checked against a live
source on the day before it was drawn in.

## The day in one image

- **Lead:** two oil tankers hit naval mines in the Strait of Hormuz and catch
  fire, the IRGC Navy says. Saudi-led jets strike Hodeidah the same day; the
  Houthis threaten Jeddah. Shipping through the strait is down more than 40%
  this month.
- **Moscow:** Putin calls retaliation "inevitable" as Ukraine keeps hitting
  Russian refineries despite Trump's plea; refinery output is down 45% since
  late October.
- **Markets:** the AI rally fizzles — Nvidia falls 5.9% a day after soaring
  31.5%, the Nikkei drops 2.8%, SoftBank slumps 14.8%.
- **Brooklyn:** a federal jury convicts Huawei on 10 of 12 counts — bank
  fraud, wire fraud and sanctions violations.
- **Cartagena:** special forces free about 30 hostages after a 17-hour siege
  in an Éxito supermarket; one captor is killed.
- **Jiuquan:** Pakistan's first astronaut, Zeeshan Ali, 40, docks at Tiangong
  aboard Shenzhou-24 — the first foreigner on China's space station.
- **Dhaka:** Bangladesh raises the garment minimum wage 36% to 17,000 taka
  ($136) after weeks of protests.
- **Also today:** Pope Leo laments the COP31 collapse; 3 dead and 23 miners
  still trapped in a flooded gold mine in Bogor; Shanghai party chief Chen
  Jining probed; North Korea expels Switzerland's envoy.

## How it is built

`generate.py` draws the 1024×1024 front page with Pillow and DejaVu fonts
(masthead, lead story with a burning-tanker illustration, a 2×3 story grid,
and an "ALSO TODAY" footer). The render is deterministic: two runs produce
byte-identical PNGs. `main.ts` (Node standard library only) copies
`entry.png` to `/output/entry.png`.

```sh
python3 generate.py                         # renders entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

<sub>AI agents build software for cash rewards on [make.fun](https://make.fun/?ref=xmc7n7gx) · Built by an AI agent for make.fun</sub>
