# ACCESS-ESM1.5 Model Configurations

## About

This repo will contain standard global configurations for ACCESS-ESM1.5, the ACCESS Coupled Earth System Model.

This is an "omnibus repository": it contains multiple related configurations, and each
configuration is stored in a separate branch.

Branches utilise a naming scheme of <<<FIXME: ADD IN NAMING SCHEME>>>.

Most configurations are adapted from work by the [CLEX CMS team](https://github.com/coecms/access-esm).

## Supported configurations

All available configurations are browsable under [the list of branches](https://github.com/ACCESS-NRI/<model>-configs/branches) and should also be listed below:

| Branch | Configuration Description |
| ------ | ------------------------- |

There are more detailed notes contained in the respective branches for each configuration.

More supported configurations will be added over time.

## How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model.

This repository contains many related experimental configurations to make support
and discovery easier. As a user it does not necessarily make sense to clone all the
configurations at once.

In most cases only a single experiment is required. If that is the case choose which experiment and then run

```sh
git clone -b <experiment> https://github.com/ACCESS-NRI/model-configs/ <experiment>
```

and replace `<experiment>` with the branch name or tag of the experiment you wish to run.

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run `<MODEL>` with `payu`](https://access-hive.org.au/models/run-a-model).

## CI and Reproducibility Checks

This repository makes use of GitHub Actions to perform reproducibility checks on model config branches.

### Config Branches

Config branches are branches that store model configurations of the form: `release-<config>` or `dev-<config>`, for example: `release-1deg_jra55_iaf`. For more information on creating your own config branches, or for understanding the PR process in this repository, see the [CONTRIBUTING.md](CONTRIBUTING.md).

### Config Tags

Config tags are specific tags on config branches, whose `MAJOR.MINOR` version compares the reproducibility of the configurations. Major version changes denote that a particular config tag breaks reproducibility with tags before it, and a minor version change does not. These have the form: `release-<config>-<tag>`, such as `release-1deg_jra55_iaf-1.2`.

So for example, say we have the following config tags:

* `release-1deg_jra55_iaf-1.0`
* `release-1deg_jra55_iaf-1.1`
* `release-1deg_jra55_iaf-2.0`
* `release-1deg_jra55_iaf-3.0`

This means that `*-1.0` and `*-1.1` are configurations for that particular experiment type that are reproducible with each other, but not any others (namely, `*-2.0` or `*-3.0`).

`*-2.0` is not reproducible with `*-1.0`, `*.1.1` or `*-3.0` configurations.

Similarly, `*-3.0` is not reproducible with `*-1.0`, `*-1.1` or `*-2.0`.

### Checks

These checks are in the context of:

* PR checks: In which a PR creator can modify a config branch, create a pull request, and have their config run and checked for reproducibility against a 'ground truth' version of the config.
* Scheduled checks: In which config branches and config tags that are deemed especially important are self-tested monthly against their own checksums.

More information on submitting a Pull Request and on the specifics of this pipeline can be found in the [CONTRIBUTING.md](./.github/CONTRIBUTING.md) and [README-DEV.md](./README-DEV.md) respectively.

For more information on the manually running the pytests that are run as part of the reproducibility CI checks, see
[model-config-tests](https://github.com/ACCESS-NRI/model-config-tests/).

## Conditions of use

<<<FIXME: ADD CONDITIONS OF USE>>>
