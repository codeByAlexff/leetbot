# LeetBot

A Discord bot that brings LeetCode problems directly into your server. Fetch specific problems, get random challenges by difficulty, view daily problems, and look up user stats — all without leaving Discord.

---

[Invite Leetbot to your server](https://discord.com/oauth2/authorize?client_id=1500224659189399765&permissions=19456&integration_type=0&scope=bot)

## Features

- Fetch any LeetCode problem by slug
- Get a random problem, optionally filtered by difficulty
- View today's daily LeetCode challenge
- Look up a LeetCode user's profile and stats
- Get hints for the last fetched problem
- Get a direct link to the last fetched problem

---

## Commands

| Command | Description |
|--------|-------------|
| `/problem <slug>` | Fetch a specific problem (e.g. `two-sum`) |
| `/random` | Get a random problem |
| `/daily` | Get today's daily LeetCode challenge |
| `/hint` | Get hints for the last fetched problem |
| `/link` | Get a direct link to the last fetched problem |
| `/user <username>` | Look up a LeetCode user's profile |
| `/help` | List all available commands |

---

## Tech Stack

- [Python](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- [Alfa LeetCode API](https://github.com/alfaarghya/alfa-leetcode-api) — Unofficial LeetCode API wrapper
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing

---

## Authors

- [@codeByAlexff](https://github.com/codeByAlexff)
