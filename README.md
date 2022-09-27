# F-Droid Scanner Signatures

NOTE: this project is just a preview, name and links will change should this
project become part of F-Droid.

This project contains signature definitions used in `fdroid scanner` command.

## Overview

The signature definitions in this project are stored in `.yml` files, analogous
to fdroiddata. The data from the YAML files gets aggregated into consolidated
JSON files.  The scripts for this process are located in the `./tools` folder
in this project.  We use GitLab Pages for assembling these JSON files and
making them easily accessible.

https://uniqx.gitlab.io/fdroid-scanner-signatures/


## Data Format

The YAML files in this project should follow this structure. Every YAML file
should roughly correspond to one software dependency, SaaS platform, etc..
They support holding multiple signatures with the goal to make long term
maintainence easy.  There is a set of specified keys in this YAML files which
are supposed to contain signatures and metadata.  They're documented in deatil
in this section.  It is also allowed to add keys/values which are not defined
here.  They may to hold additional informations about the software dependency
but will be ingored by `fdroid scanner`.

### `code_signatures`

A list of (python) regular expressions. Binaries (eg. APK files) will be
scanned for these signatures.

example:

```yaml
code_signatures:
  - com/example/analytics
```

### `gradle_signatures`

A list of (python) regular expressions. Gradle files will be scanned for these
signatures.

example:

```yaml
gralde_signatures:
 - example\.com:evil-lib
 - example\.com:bad-lib
```

### `license`

The license of this software dependency. Use [SPDX
idnetifier](https://spdx.org/licenses/) for FOSS dependencies. For proprietary
dependencies just put `NonFree` as license value.

example:

```yaml
license: NonFree
```

## Cache Data Format

The cache data format is directly derived from the Data Format specified above.
It's basically combining all yaml files in a foldler into a single json file
and adds a version number (integer) and a timestamp (iso8601 with explicit
timezone). It also contains an object called signatures which has the names of
all YAML files as keys an their contents as value. For readability and pleasing
git-diffs, these json files are typically formated with 2 space indent per
level.

example:

```json
{
  "signatures": {
    "example.com": {
      "gradle_signatures": [
        "com\\\\.example:evil-lib",
        "com\\\\.example:bad-lib"
      ],
      "license": "NonFree"
    },
    "com.google.analytics": {
      "code_signatures": [
        "com/google/analytics"
      ],
      "license": "NonFree"
    }
  },
  "timestamp": "1999-12-31T23:59:59.999999+00:00",
  "version": 1
}
```
