<a className="gh-badge" href="https://datahub.io/core/population"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

Population figures for countries, regions (e.g. Asia) and the world. Data comes
originally from World Bank and has been converted into standard CSV.

## Data

The data is sourced from this [World Bank dataset][wb] which in turn lists as
sources: *(1) United Nations Population Division. World Population Prospects,
(2) United Nations Statistical Division. Population and Vital Statistics Reprot
(various years), (3) Census reports and other statistical publications from
national statistical offices, (4) Eurostat: Demographic Statistics, (5)
Secretariat of the Pacific Community: Statistics and Demography Programme, and
(6) U.S. Census Bureau: International Database.*

[wb]: http://data.worldbank.org/indicator/SP.POP.TOTL

## Preparation

The `population.csv` is processed using `scripts/process.py` script.

```
    pip install -r scripts/requirements.txt
    python scripts/process.py
```

## Automation

Up-to-date (auto-updates on quarterly basis) population dataset could be found on the datahub.io:
https://datahub.io/core/population

## License

This Data Package is licensed by its maintainers under the [Public Domain Dedication and License (PDDL)](http://opendatacommons.org/licenses/pddl/1.0/).