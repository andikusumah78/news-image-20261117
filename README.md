[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/andikusumah78/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/andikusumah78/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# Sum up 17 November's world news in one image

make.fun bounty entry: [news-image-20261117](https://make.fun/bounty/news-image-20261117)

A newspaper front page that sums up Tuesday 17 November 2026's world news
in one image, drawn programmatically with Pillow (`tools/make_image.py`).

## The stories

1. **Kerch Bridge hit — road span collapses.** Ukraine strikes the bridge
   linking Russia to occupied Crimea again; a road span collapses. Russia
   hits Kyiv's bridges over the Dnipro with ballistic missiles.
   (BBC, Al Jazeera, Reuters)
2. **Trump in Manila.** President Trump arrives in the Philippines for the
   ASEAN summit, the first stop of a three-day Asia trip; a three-way meeting
   with Xi Jinping and Vladimir Putin is set for Thursday in Shenzhen.
   (Associated Press)
3. **Tankers hit by mines.** Two oil tankers strike mines and catch fire near
   the Strait of Hormuz; a third US aircraft carrier arrives in the region.
   (Al Jazeera, Reuters, PBS NewsHour)
4. **Vulcan rocket fails.** A ULA Vulcan rocket fails in flight, destroying
   40 Amazon Leo internet satellites. (Spaceflight Now)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `assets/entry.png`
to `/output/entry.png` byte for byte, so two runs write identical bytes.
The image is 1024x1024 PNG, well under the 1 MiB limit.

## License

MIT — see `LICENSE`.
