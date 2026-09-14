# AGENTS.md

Guidance for coding agents working from this downloaded Coworld package.

## Facts

- Champion means your nominated policy version: the chosen participant you want to represent you in a league. It is not
  a claim that the policy has won the tournament.

## Start

- Read the league participation guide before entering a league:
  - Gods of the Arena: https://softmax.com/api/observatory/v2/participate?league_id=league_3c60897b-25cf-4b37-9d1a-8554c1198f28
- Read `coworld_manifest.json` before changing policy code.
- Treat `game.protocols.player`, `game.docs.pages`, `variants`, and `certification` as the local contract for this
  package.
- Run `uv run coworld run-episode ./coworld_manifest.json --timeout-seconds 120` with the bundled players before
  testing your own image.

## Policy Work

- Keep policy source in your policy project, not in this downloaded Coworld cache.
- Use the manifest path from this directory when building, running, and comparing policies.
