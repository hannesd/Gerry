[![Build Status](https://travis-ci.org/michaeldorner/Gerry.svg)](https://travis-ci.org/michaeldorner/Gerry) 
[![codecov](https://codecov.io/gh/michaeldorner/Gerry/branch/master/graph/badge.svg)](https://codecov.io/gh/michaeldorner/Gerry)
[![codebeat badge](https://codebeat.co/badges/f8306b22-3837-4244-a637-e880c6532700)](https://codebeat.co/projects/github-com-michaeldorner-gerry-master)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)

# Gerry

> Gerry is a small utility written in Python to crawl Gerrit review instances. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Gerrit API](#api)
- [Contributions](#contributions)
- [Versions](#versions)
- [License](#license)


## Installation

Two packages are required: [`tdqm`](https://github.com/noamraph/tqdm) for a nice progress bar and [requests](https://github.com/requests/requests) for handling the HTTP requests. You can use pip for installing these required packages:

    pip install -r requirements.txt


## Usage

    python gerry.py <gerrit_instance> [--directory=<storage_directory>]
    
* `<gerrit_instances>`: Gerry supports the gerrit instances of OpenStack (`openstack`), Chromium (`chromium`), Gerrit (`gerrit`), Android ('android'), Go (`golang`), LibreOffice (`libreoffice`), Eclipse (`eclipse`), Wikimedia (`wikimedia`), and ONAP (`onap`). 
* `<storage_directory>` (optional): The storage directory where to store the files (default `./gerry_data/`).


## Discussion
Gerry is the only Gerrit crawling tool (to my knowledge) which is not affected by the [Bug 9835](https://bugs.chromium.org/p/gerrit/issues/detail?id=9385). 


## Contributions

### To-do

It would be great to get a pull request containing new instances or adding the option to add own (private, non-open-source) instances. 


### Acknowledgements

Many thanks to my great master student Jonathan Rieß, who added the tests. 


## Versions
1.0


## License 

Gerry is released under the MIT license. See [LICENSE](LICENSE) for more details.
