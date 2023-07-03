# asana-to-things
Python script for adding Asana CSV project export to Things3 on Mac, using [Things URLs](https://culturedcode.com/things/blog/2018/02/hey-things/).

Author: [Ryan Steed](https://rbsteed.com)

## Installation
1. `make venv`
2. Copy Things URL token from Settings -> General -> Enable Things URLs -> Manage and store in `token.json` as `{"token": <token>}`.

## Usage
1. Export an Asana project to CSV.
2. `python import.py import_asana <Path to CSV> --name <Project Name>`
