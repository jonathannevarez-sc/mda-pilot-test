# mda-pilot-test

A Python package for the Dispatch team's stop order: the planned stop order for a
day, the moment a truck is loaded, and what the driver sees on the device.

## Layout

- `dispatch/` — the modules the stories change
- `tests/` — unittest tests, one per acceptance line

## Tests

```
python3 -m unittest discover -s tests
```

Standard library only. No third-party packages.
