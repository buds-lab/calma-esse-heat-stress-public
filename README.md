# Calma-esse-heat-stress-internal


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Project Description">About The Project</a>
      <ul>
        <li><a href="#Calma">Calma</a></li>
        <li><a href="#Esse">Esse</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Prerequisites">Prerequisites</a></li>
        <li><a href="#Installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#License">License</a></li>
    <li><a href="#Contact">Contact</a></li>
    <li><a href="#Acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is part of a Masterthesis of [Ben Gottkehaskamp](https://github.com/benterich) at the [Chair for Building Technology and Climate Responsive Design](https://www.arc.ed.tum.de/en/klima/start/) at the [Technical University of Munich (TUM)](https://www.tum.de/en/) and in cooperation with the [budslab](https://budslab.org/) at the National [University of Singapore (NUS)](https://nus.edu.sg/).

### Calma

'Calma' is the debugging phase of this project, which consisted of two subprojects. One testing the final study procedure for 'Esse' and one to test features like the geolocation features.

#### Calma debugging

need to fill up

#### Geo-location testing
This survey serves as a validation tool for assessing the geospatial capabilities of Cozie. Its purpose is to conduct multiple passes along specific routes to identify discrepancies in longitude and latitude data, while also incorporating supplementary metadata for in-depth analysis of various influences. The primary focus is on outdoor locations and travel patterns following periods spent indoors. Besides the retreived Cozie data the following features are available in form of survey data: `tag/q_location_area` `tag/q_location_time` `tag/q_connection_network` `tag/q_connection_people` `tag/q_envi_traversion` `tag/q_envi_sky` `tag/q_envi_rain`, as well as some additional features that categorize the run like `tag/q_study` `tag/q_study_amount` `tag/q_study_setpoint`.

### Esse


### Built With

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

## Getting Started

### Prerequisites
- Create and activate a virtual Python environment.
- Install the `requirements.txt`:
```py
pip install -r /path/to/requirements.txt 
```

#### versionDisplay
Check via cmd 'pip list' your current version installed.

```bash
coziepy       ==0.0.15
DateTime      ==5.2
geopandas     ==0.13.2
jupyter_core  ==5.3.2
matplotlib    ==3.7.2
numpy         ==1.25.2
pandas        ==2.1.0
plotly        ==5.16.1
requests      ==2.31.0
seaborn       ==0.12.2
```

### Installation
 - Clone the repository
 - Follow the Prerequisites steps
 - Setup the config.py file wit the following inputs under Esse\src\config.py

 '''py
 API_KEY  = #Enter Your API Key here. It is provided by the [Cozie](https://cozie-apple.app). Please contact us at cozie.app@gmail.com if you need one. 
 '''

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Acknowledgments

Thank you for your contributions and support in this project:

- [Ben Gottkehaskamp](https://github.com/benterich) (creator)