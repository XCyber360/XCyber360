---
name: New release
about: "[xcyber360-team] Track the effort of the team to release a new version of Xcyber360"
title: Support for Xcyber360 4.x.x
labels: enhancement
assignees: ''

---

## Description

Example:
> Xcyber360 4.3.8 will be released shortly. Our Xcyber360 Dashboard and Kibana apps need to support this new version. From our side, no changes will be included, so we only need to bump the version.


## Tasks

### Pre-release
- [ ] Add support for Xcyber360 4.x.x (bump).
- [ ] Generate the required tags.
- [ ] Generate the packages.
- [ ] Test the packages, to verify they install, and the app works as expected.
- [ ] [Optional] Run Regression Testing (#issue) 
- [ ] Generate draft releases.
- [ ] Notify the @xcyber360/cicd and @xcyber360/content teams that the release is good to go, from our side.

### Post-release
- [ ] Make draft releases final and public.
- [ ] Sync branches.
- [ ] Update [Compatibility Matrix](https://github.com/xcyber360/xcyber360-kibana-app/wiki/Compatibility).

### Supported versions

Same as on [previous releases](https://github.com/XCyber360/XCyber360/tree/master/dashboard/plugins/wiki/Compatibility)
