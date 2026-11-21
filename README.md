# The World in One Day — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/anggianugrah214-eng/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/anggianugrah214-eng/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page for Friday 20 November 2026, drawn
entirely in code with Python and Pillow (`draw_image.py`, 1024 × 1024).
No photographs or outside images: the map, the bridge, the market chart,
the flags, the tower and the cyclone are all drawn from shapes and text.

## The stories on the page

1. **Lead — Russian missiles strike Poland.** Two missiles and a
   suspected drone come down on Polish soil; Warsaw calls it a deliberate
   provocation, NATO calls it a grave violation of allied airspace, and
   NATO jets scramble.
2. **Kyiv bridges hit.** Overnight Russian strikes kill 3, damage two
   bridges and cut power in the Ukrainian capital.
3. **Shares tumble.** The S&P 500 falls 3.7% and the Nikkei 5.1% as AI
   worries drag markets down for a sixth straight day; Anthropic slides
   on day two after its record debut.
4. **Brexit reset deal.** Britain and the EU agree deals on food trade,
   carbon markets and youth mobility at their Brussels summit.
5. **Tower hit in Riyadh.** A Houthi strike hits the PIF Tower in the
   Saudi capital.
6. **Cyclone Akvan.** The storm makes landfall on India's Odisha coast;
   a magnitude 6.7 earthquake shakes central Peru.

The footer ticker adds the day's other news: rights groups urging
sanctions after the world court's genocide ruling, the COP31 final text
dropping "fossil fuels", the Palisades arson verdict, Bayer's $7.25bn
Roundup settlement, GTA VI's $3.79bn first-day sales record, and
BepiColombo reaching Mercury.

## Running it

```sh
python3 draw_image.py                 # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/
```

`main.ts` is the entrypoint: it copies the image the repository holds
into the output directory as `entry.png`. Running it twice writes
identical bytes.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=64yv74h6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
