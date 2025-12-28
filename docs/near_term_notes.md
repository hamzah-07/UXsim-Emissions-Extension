# Near-Term Notes

This is just a working note for the next chunk of the project. It is not meant to be
formal or final, just enough to keep the next few commits pointed in the right
direction.

## Where We Are

We now have the first proper end-to-end slice in place:

- UXsim smoke world and snapshot capture
- vehicle and link observations
- starter factor loading
- first average-speed CO2 model
- snapshot interval runner

That is a good base. The next job is to turn it into something a bit more usable and
less "tests only".

## Next Few Commits

- Add a tiny experiment script that runs the smoke world over two snapshots and prints
  the interval emissions result in a way that is easy to eyeball.
- Add one small helper for turning a run into multiple interval results, not just a
  single pair of snapshots.
- Start recording interval outputs in a simple structure that could later be written to
  CSV without much fuss.

## Model Follow-Up

- Replace the starter factor table with something more defensible once the proper
  literature-backed source is chosen.
- Decide how we want to handle speeds outside the known factor range in the final
  version. Clamping is fine for now, but probably not the last word.
- Revisit acceleration later once the average-speed path is settled. No point making
  that messy too early.

## Integration Follow-Up

- Check whether we want interval emissions based on snapshot pairs only, vehicle logs,
  or a mix of both.
- Confirm what should happen when vehicles appear or disappear between snapshots, and
  make sure that stays deliberate rather than accidental.
- Eventually add per-link rollups, because right now the focus is mostly on
  per-vehicle interval output.

## Validation and Data Notes

- Pick the first real source for CO2 factors and write down exactly what was used.
- Keep a note of unit assumptions everywhere. This will save pain later.
- Once a real dataset is in, add one or two sanity-check tests against values we expect
  from the source rather than just the starter CSV.

## Scenario Notes

- Keep using the tiny smoke world for quick checks.
- After that, add one slightly richer toy network before jumping straight to OSM.
- Do not rush the town-centre case study until the output format and model behaviour
  feel stable.

## General Reminders

- Keep commits small and boring where possible.
- Add comments when the code is doing something a bit subtle, not just because we can.
- Leave obvious WIP notes in places where future-us might otherwise waste half an hour
  re-deriving the intent.
- Do a quick maintenance pass every few feature commits rather than waiting until the
  code feels messy.

## Nice-to-Have Soon

- A short glossary note for terms like snapshot, interval, factor table, and vehicle
  observation.
- A simple path for exporting results to CSV.
- A tiny benchmark or timing check so we notice early if the model path starts getting
  too heavy.
