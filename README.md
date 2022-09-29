# SUSS - Suspicious or Unwanted Software Signatures

NOTE: this project is just a preview, name and links will change should this
project become part of F-Droid.

This project contains signature definitions used in `fdroid scanner` command.

## Overview

The signature definitions in this project are stored in `.yml` files, analogous
to fdroiddata. ([signature
definitions](https://gitlab.com/fdroid/suss/-/tree/master/suss))

The data from these YAML files gets aggregated into the JSON file format
`fdroid scanner` is using.  F-Droid Scanner can consume multiple of these JSON
files.  We use GitLab Pages for assembling these JSON files and making them
easily accessible. ([generated json
files](https://fdroid.gitlab.io/suss))  The scripts for
this process are located in the `./tools` folder in this project.  We can also
convert signatures from 3rd party sources (e.g. izzy) and convert them to
F-Droid Scanners JSON format.


## Data Format of Signature Definitions

The YAML files in this project should follow this structure. Every YAML file
should roughly correspond to one software dependency, SaaS platform, etc..
They support holding multiple signatures with the goal to make long term
maintenance easy.  There is a set of specified keys in this YAML files which
are supposed to contain signatures and metadata.  They're documented in detail
in this section.  It is also allowed to add keys/values which are not defined
here.  They may to hold additional informations about the software dependency
but will be ignored by `fdroid scanner`.

### `code_signatures`

A list of (python) regular expressions. Binaries (e.g. APK files) will be
scanned for these signatures.

example:

```yaml
code_signatures:
  - com/demo/analytics
```

### `gradle_signatures`

A list of (python) regular expressions. Gradle files will be scanned for these
signatures.

example:

```yaml
gradle_signatures:
 - example\.com:evil-lib
 - example\.com:bad.*lib
```

### `license`

The license of this software dependency. Use [SPDX
identifier](https://spdx.org/licenses/) for FOSS dependencies. For proprietary
dependencies just put `NonFree` as license value.

example:

```yaml
license: NonFree
```

### `warn_code_signatures`

Same as `code_signatures` but issues a warning instead of an error.

example:

```yaml
warn_code_signatures:
 - com/demo/.*metrics
```

### `warn_gradle_signatures`

Same as `gradle_signatures` but issues a warning instead of an error.

```yaml
warn_gradle_signatures:
 - com\.example:ads
```

## Cache-File Data Format

The cache data format is directly derived from the Data Format specified above.
It's basically combining all YAML files in a folder into a single JSON file
and adds a version number (integer) and a timestamp (ISO8601 with explicit
timezone). It also contains an object called signatures which has the names of
all YAML files as keys an their contents as value. For readability and pleasing
git-diffs, these JSON files are typically formated with 2 space indent per
level.

example:

```json
{
  "signatures": {
    "example.com": {
      "gradle_signatures": [
        "com\\\\.example:evil-lib",
        "com\\\\.example:bad.*lib"
      ],
      "warn_gradle_signatures": [
        "com\\\\.example:ads",
      ],
      "license": "NonFree"
    },
    "demo.com": {
      "code_signatures": [
        "com/demo/analytics"
      ],
      "warn_code_signatures": [
        "com/demo/.*metrics"
      ],
      "license": "NonFree"
    }
  },
  "timestamp": "1999-12-31T23:59:59.999999+00:00",
  "version": 1
}
```

The key names for entries in `"signatures"` correspond to YAML file names. So
for the above example would be the result of two files called:
_example.com.yml_ and _demo.com.yml_.
