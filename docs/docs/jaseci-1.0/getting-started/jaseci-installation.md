---
sidebar_position: 4
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Jaseci Installation


<Tabs>
  <TabItem value="macos-and-windows-wsl" label="Windows (WSL)" default>
    <h2>Windows Set up</h2>
    <h3>Software Requirements</h3>
    <ul>
    <li>Ubuntu 20 +</li>
    <li>Code Editor (We Recommend VS code)</li>
    </ul>
    <h3>Install Ubuntu Command Line</h3>
      <ul>
    <li>Open the Windows Powershell Command Line in adminstrator mode</li>
    <li>Run the Following command :  <pre><code>wsl --install</code></pre> </li>
    <li>Restart your computer</li>
    <li>Open the Ubuntu terminal which comes as the default. For more info see <a href="https://docs.microsoft.com/en-us/windows/wsl/install">here</a></li>
    </ul>
    <h3>Install Visual Studio Code</h3>
     <p>We recommend the Use of Visual studio code as there is JAC extension avaliable</p>
    <ul>
    <li>Install Visual Studio code <a href="https://code.visualstudio.com/download">here</a></li>
    <li>Once the download is completed open Visual studio code</li>
    
<h2>Install Python and pip</h2> 
    <ol>
        <li> Check if python is installed by running the following in the ubuntu terminal: <pre><code>python --version</code></pre>   </li>
        <li> If it returns 3.8 or higher go to Jaseci Installation</li> 
        <li> If "python3: commmand not found" shows up you have to install python. Run : <pre><code> sudo apt install python3 python3-pip</code></pre></li>
        <li>To instal python3 run <strong>sudo apt install python3 python3-pip</strong></li>
        </ol>
    </ul>

  </TabItem>
  <TabItem value="linux" label="Linux">
  <h2>Linux and OS </h2>
  <p>The command line is capable of handling bash arguments so all you need to do is install python and the pip package Manager </p>
   <h3>Install Visual Studio Code</h3>
     <p>We recommend the Use of Visual studio code as there is JAC extension avaliable</p>
    <ul>
    <li>Install Visual Studio code <a href="https://code.visualstudio.com/download">here</a></li>
    <li>Once the download is completed open Visual studio code</li>
    </ul>
   
  </TabItem>
</Tabs>
      <h2>Installing Jaseci and Jaseci Kit</h2>
      <ol>
      <p>Now that we have Python and pip installed let's install Jaseci.</p>
        <li> run : <pre><code>pip install jaseci</code></pre></li>
        <li>Now to install the Jaseci Kit run : <pre><code>pip install jaseci-kit</code></pre></li>
         <li>Ensure your Installation is complete by running: <pre><code>jsctl</code></pre> . It that shows a list of options and commands you're installation is complete</li>  
    </ol>