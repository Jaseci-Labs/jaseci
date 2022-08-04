# JAC Build Pipeline

Description of JAC pipeline into Azure DevOps.

## Sentinel Registered on the Server - Manual Process

1. Run the script into bash shell.

```bash
pip install jaseci   # install jaseci
jsctl login <url>  --username <username> --password <password>  # login to Jaseci
jsctl sentinel set <jacCode> -mode code  # set sentinel  with jac file (e.g 'zsb.jac')
jsctl sentinel active get > sentinel.json  # Store the sentinel data into  'sentinel.json' file
```

2. Copy 'sentinel.json' file from pipeline env to build artifacts staging directory e.g '$(Build.ArtifactStagingDirectory)'

```bash
- task: CopyFiles@2
  inputs:
    Contents: '**/sentinel.json' // Copied file
    TargetFolder: '$(Build.ArtifactStagingDirectory)'
```

3. Publish '$(Build.ArtifactStagingDirectory)' artifact.

```bash
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'  //// artifacts staging directory
    ArtifactName: '<ArtifactName>' // Name of Published Artifact
    publishLocation: 'Container'
```

## Extract the ".jac" Code from Repo


1. Copy '.jac' file from repo to build artifacts staging directory e.g '$(Build.ArtifactStagingDirectory)'

```bash
- task: CopyFiles@2
  inputs:
    Contents: '**/<jacFile>'
    TargetFolder: '$(Build.ArtifactStagingDirectory)'
```

2. Publish '$(Build.ArtifactStagingDirectory)' artifact.

```bash
- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'  //// artifacts staging directory
    ArtifactName: '<ArtifactName>' // Name of Published Artifact
    publishLocation: 'Container'
```
