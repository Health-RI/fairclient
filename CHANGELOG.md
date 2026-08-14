# Changelog

All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v1.0.3] - 2026-08-14

### Added
- feat: hard code version by @TimVanMourik in ab12e82
- feat: expose MongoDB port in dev setup by @Alexander Harms in 20cae9e
- feat: add single-FDP development setup by @Alexander Harms in e33a7be


### Changed
- docs: adds FDP support version by @Alexander Harms in 60a729a
- build(deps): bump actions/setup-python from 6 to 7 by @dependabot[bot] in 8176d00
- refactor: remove dev workarounds by @TimVanMourik in 95d9e53
- docs: simplifies readme by @Alexander Harms in c2ac7bc
- build(deps): bump pypa/gh-action-pypi-publish from 1.14.0 to 1.14.2 by @dependabot[bot] in 394b8a8
- build(deps): bump SonarSource/sonarqube-scan-action from 8.0.0 to 8.2.1 by @dependabot[bot] in 493391c
- build(deps): bump actions/checkout from 6 to 7 by @dependabot[bot] in cb453a5
- build(deps): bump actions/upload-artifact from 4 to 7 by @dependabot[bot] in fa6c6e5
- build(deps): bump actions/checkout from 4 to 6 by @dependabot[bot] in e302acb
- build(deps): bump pypa/gh-action-pypi-publish from 1.12.4 to 1.14.0 by @dependabot[bot] in 1abb2a6
- build(deps): bump actions/setup-python from 5 to 6 by @dependabot[bot] in 8ad73c2
- build(deps): bump SonarSource/sonarqube-scan-action from 7.0.0 to 8.0.0 by @dependabot[bot] in 4cd04c6
- build(deps): bump actions/download-artifact from 5 to 8 by @dependabot[bot] in d138190
- build(deps): update rdflib requirement from <7.2,>=7.0 to >=7.0,<7.7 by @dependabot[bot] in 7bdf8e7
- ci: sync python-test action with organisation default by @kburger in a7aa216
- ci: sync sonar properties with organisation defauls by @kburger in c2e3e20
- doc: update CHANGELOG.md for v1.0.2 by @Health-RI Admin in 4667237


### Fixed
- fix: adds quotes to version string by @Alexander Harms in b8587b3
- fix: adds test with leading slash by @Alexander Harms in b6daed6
- fix: adds missing dependency by @Alexander Harms in fa7cc99
- fix: re-anchor FDP record URIs onto the client base URL by @Alexander Harms in 861f25d
- fix(ci): update ci dependencies by @Alexander Harms in 3e0d1f4
- fix(ci): publish pypi on workflow dispatch, test on PR ready to review by @Alexander Harms in 3af89e5


### Removed
- style: remove commented lines from action by @kburger in 7ab1c4a


## [v1.0.2] - 2025-07-07

### Changed
- ci: adds release and test workflow by @Alexander Harms in e48c98b
- Bump pypa/gh-action-pypi-publish from 1.12.3 to 1.12.4 by @dependabot[bot] in 89801e8
- Bump pypa/gh-action-pypi-publish from 1.11.0 to 1.12.3 by @dependabot[bot] in 15e25c6
- Bump codecov/codecov-action from 4 to 5 by @dependabot[bot] in 075496d
- Bump pypa/gh-action-pypi-publish from 1.10.3 to 1.11.0 by @dependabot[bot] in cdf72ac
- Update rdflib requirement from ~=7.0.0 to >=7.0,<7.2 by @dependabot[bot] in 8de7d09
- Bump pypa/gh-action-pypi-publish from 1.10.2 to 1.10.3 by @dependabot[bot] in ed1371d


### Fixed
- ci: update pyproject.toml to fix test by @Alexander Harms in f7a83ad


