# Xcyber360 Filebeat module

## Hosting

The Xcyber360 Filebeat module is hosted at the following URLs

- Production:
  - https://packages.xcyber360.com/4.x/filebeat/
- Development:
  - https://packages-dev.xcyber360.com/pre-release/filebeat/
  - https://packages-dev.xcyber360.com/staging/filebeat/

The Xcyber360 Filebeat module must follow the following nomenclature, where revision corresponds to X.Y values

- xcyber360-filebeat-{revision}.tar.gz

Currently, we host the following modules

|Module|Version|
|:--|:--|
|xcyber360-filebeat-0.1.tar.gz|From 3.9.x to 4.2.x included|
|xcyber360-filebeat-0.2.tar.gz|From 4.3.x to 4.6.x included|
|xcyber360-filebeat-0.3.tar.gz|4.7.x|
|xcyber360-filebeat-0.4.tar.gz|From 4.8.x to current|


## How-To update module tar.gz file

To add a new version of the module it is necessary to follow the following steps:

1. Clone the xcyber360/xcyber360 repository
2. Check out the branch that adds a new version
3. Access the directory: **extensions/filebeat/7.x/xcyber360-module/**
4. Create a directory called: **xcyber360**

```
# mkdir xcyber360
```

5. Copy the resources to the **xcyber360** directory

```
# cp -r _meta xcyber360/
# cp -r alerts xcyber360/
# cp -r archives xcyber360/
# cp -r module.yml xcyber360/
```

6. Set **root user** and **root group** to all elements of the **xcyber360** directory (included)

```
# chown -R root:root xcyber360
```

7. Set all directories with **755** permissions

```
# chmod 755 xcyber360
# chmod 755 xcyber360/alerts
# chmod 755 xcyber360/alerts/config
# chmod 755 xcyber360/alerts/ingest
# chmod 755 xcyber360/archives
# chmod 755 xcyber360/archives/config
# chmod 755 xcyber360/archives/ingest
```

8. Set all yml/json files with **644** permissions

```
# chmod 644 xcyber360/module.yml
# chmod 644 xcyber360/_meta/config.yml
# chmod 644 xcyber360/_meta/docs.asciidoc
# chmod 644 xcyber360/_meta/fields.yml
# chmod 644 xcyber360/alerts/manifest.yml
# chmod 644 xcyber360/alerts/config/alerts.yml
# chmod 644 xcyber360/alerts/ingest/pipeline.json
# chmod 644 xcyber360/archives/manifest.yml
# chmod 644 xcyber360/archives/config/archives.yml
# chmod 644 xcyber360/archives/ingest/pipeline.json
```

9. Create **tar.gz** file

```
# tar -czvf xcyber360-filebeat-0.4.tar.gz xcyber360
```

10. Check the user, group, and permissions of the created file

```
# tree -pug xcyber360
[drwxr-xr-x root     root    ]  xcyber360
├── [drwxr-xr-x root     root    ]  alerts
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  alerts.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  archives
│   ├── [drwxr-xr-x root     root    ]  config
│   │   └── [-rw-r--r-- root     root    ]  archives.yml
│   ├── [drwxr-xr-x root     root    ]  ingest
│   │   └── [-rw-r--r-- root     root    ]  pipeline.json
│   └── [-rw-r--r-- root     root    ]  manifest.yml
├── [drwxr-xr-x root     root    ]  _meta
│   ├── [-rw-r--r-- root     root    ]  config.yml
│   ├── [-rw-r--r-- root     root    ]  docs.asciidoc
│   └── [-rw-r--r-- root     root    ]  fields.yml
└── [-rw-r--r-- root     root    ]  module.yml
```

11. Upload file to development bucket
