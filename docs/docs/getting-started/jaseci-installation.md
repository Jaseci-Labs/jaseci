---
side_bar_position: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Jaseci Installation

## Software Requirements

- Docker Desktop (Latest)
- Kubernetes CLI (Comes as part of Docker Desktop)



<Tabs>
  <TabItem value="macos-and-windows-wsl" label="MacOS and Windows (WSL)" default>
    <h2>Setup Jaseci Repository</h2>
    <p>Clone the Jaseci repo at https://github.com/Jaseci-Labs/jaseci.git</p>
    <h2>Configuring Docker Desktop</h2>
    <ul>
        <li>Launch Docker Desktop</li>
        <li>Click the Gear/ Settings icon on the top right</li>
        <li>Click the resources tab on the left, then adjust the controls as follows</li>
        <li>The minimum number of CPU's should be set to <strong>4</strong>.</li>
        <li>The minimum amount of Memory should be set to <strong>4</strong>.</li>
        <li>The minimum amount of Swap Memory should be set to <strong>1</strong>.</li>
        <li>The minimum Disk image size should be set to <strong>59.6 GB</strong>.</li>
        <li>Click the Kubernetes tab on the left, Then check the first box (Enable Kubernetes) to enable Kubernetes.</li>
        <li>Click the Apply and Restart button to the bottom right, then allow for Docker Desktop to sucessfully restart.</li>
    </ul>
    <h2>Kubernetes CLI</h2>
    <p>Kubernetes CLI comes installed as part of the Docker Desktop Application. You can however skip this test if you can successfully run the following command:</p>
    <pre><code>which kubectl</code></pre>
    <p>This should print the following:</p>
    <pre><code>/usr/local/bin/kubectl</code></pre>
    <p>If the above command does not work you can either download the latest version of the Docker Desktop Application or reinstall the latest version if you are already up to date on the latest one. If the above options are not somehow available to you, proceed to the following steps below.</p>
    <h3>Steps</h3>
    <ol>
        <li>Install Homebrew if its not already installed on your Mac (MacOS Only).</li>
        <li>Install Kubernetes CLI by running the following command (MacOS Only):</li>
        <br/>
        <pre><code>brew install kubernetes-cli</code></pre>
        <li>Verify that Kubernetes CLI is sucessfully installed by running the following command:</li>
        <br/>
        <pre><code>which kubectl</code></pre>
        <li>The above should output: <code>/usr/local/bin/kubectl</code></li>
        <li>Configure kubectl to use the Docker Desktop Application by running the following command:</li>
        <br/>
        <pre><code>kubectl config use-context docker-desktop</code></pre>
    </ol>
  </TabItem>
  <TabItem value="linux" label="Linux">
    <h2>Setup Jaseci Repository</h2>
    <p>Clone the Jaseci repo at https://github.com/Jaseci-Labs/jaseci.git</p>
    <ol>
        <li>Follow steps 1 through 5 <a href="https://phoenixnap.com/kb/install-kubernetes-on-ubuntu">here</a> to install Docker, Kubernetes and Kubectl on your Machine. Please use your package manager if you do not have apt.</li>
    </ol>
  </TabItem>
</Tabs>
