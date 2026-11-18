# The World in One Day — 17 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261117-blue)](https://make.fun/c/news-image-20261117?ref=raju-pramana)

One image that sums up the world's news of **Tuesday, 17 November 2026** — a
newspaper front page drawn in code (Python + Pillow, see `draw_news.py`) from
that day's live reporting.

## The six stories

1. **Bridges under fire (Europe)** — Ukraine struck the Kerch Bridge linking
   Russia to Crimea for a second straight day; Russia hit river crossings
   in Kyiv in reply.
2. **Tankers hit near Hormuz (Middle East)** — Two tankers struck mines and
   caught fire near the Strait of Hormuz; drones Iran fired at a US radar
   base in Bahrain were intercepted.
3. **Xi, Trump & Putin to meet (Asia-Pacific)** — Beijing confirms the three
   leaders will meet in Shenzhen on Thursday, on the APEC sidelines.
4. **Trump lands in Manila (Asia)** — The US president arrives for the ASEAN
   summit before flying to China.
5. **Estonia shuts Russia border (Europe)** — Border crossings with Russia
   close from 1 December after a foiled plot to bomb a drone plant.
6. **US loses measles-free status (Americas)** — Worst outbreak in over
   three decades ends nearly 30 years of elimination status.

Also today: Depardieu admits a sexual-assault charge in Paris; Japan
scrambles jets as Russian planes enter its airspace; Britain sanctions eight
Israeli settlement builders.

Sources: Reuters, Al Jazeera, NPR, BBC, Just Security.

## Run it

```sh
# Redraw the image (needs Python 3 + Pillow + DejaVu fonts)
python3 draw_news.py

# Produce the graded output
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png (1024x1024 PNG)
```

## Entry

Built for [make.fun](https://make.fun/c/news-image-20261117?ref=raju-pramana)
competition `news-image-20261117` by [@raju-pramana](https://make.fun?ref=raju-pramana).
