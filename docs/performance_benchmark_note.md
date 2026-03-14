# Performance Benchmark Note

This note records the first performance and stability read-out for the current
UXsim emissions extension.

The purpose of this step is to document how much runtime overhead the current
emissions models add relative to plain UXsim, using both a small validation
network and the Linlithgow town-centre case study.

## Benchmark scope

The current benchmark scripts cover:

- plain UXsim on the small validation network
- plain UXsim on the Linlithgow baseline case study
- UXsim plus the average-speed model
- UXsim plus the speed-acceleration model

For the Linlithgow benchmark, the emissions-enabled runs use the same light
logging settings as the main case-study script:

- `per_timestep=False`
- `per_vehicle=False`
- `per_link=False`

This keeps the benchmark focused on model overhead rather than on the extra
cost of retaining large high-frequency output structures.

## Small-network benchmark caveat

Single-shot timings on the small validation network were too noisy to support
strong conclusions. In one recorded run, the emissions-enabled paths appeared
faster than plain UXsim, which is not a credible performance finding and is
better interpreted as timing noise on a very small scenario.

The small-network benchmark is therefore useful as plumbing and as a smoke
check that the comparison path works, but it should not be treated as the main
performance evidence for the dissertation.

## Linlithgow baseline benchmark

One recorded Linlithgow baseline benchmark run produced the following results:

- plain UXsim: `1.335 s`
- average-speed model: `1.434 s` (`1.07x` plain UXsim)
- speed-acceleration model: `1.385 s` (`1.04x` plain UXsim)

These figures suggest that both current emissions models add only modest
runtime overhead on the medium-sized case-study network.

## Stability

No obvious stability issues were observed during the current benchmark runs.
The small-network and Linlithgow benchmark paths both completed successfully,
and the emissions-enabled Linlithgow case study remained comfortably feasible
to run on this machine.

## Practical threshold and optimisation focus

For this project, a practical warning threshold is any sustained case-study
runtime above roughly `2x` the plain UXsim baseline. The current Linlithgow
results are well below that threshold.

The main avoidable performance risk is likely to be retained high-frequency
logging rather than the emissions maths alone, especially when combining:

- per-timestep retention
- per-vehicle retention
- per-link retention

If later scenarios or analysis runs become noticeably slower, those logging
settings should be the first place to look for optimisation before attempting
deeper model changes.

## Current interpretation

At this stage, the average-speed and speed-acceleration models both appear
feasible for the planned dissertation case study. The benchmark evidence is
strongest on the Linlithgow network, while the small-network timing remains
too noisy to carry much analytical weight on its own.
