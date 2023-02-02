# Introduction
  
Aims at [美姿图](https://mmzztt.com/), 
which allows users to view upto 15 images per album 
from the browser (unlimited in its mobile App)
  
# Specification
> Built on `macOS 13.1`  
> with os built-in `Python: 3.9.6`  
> utilising `scrapy` `pillow` `selenium`  
  
# Contents
Contains two scrapy projects:  
- `mzt_model` starting with the page [模特](https://mmzztt.com/photo/model/)  
- `mzt_top` starting with the page [最热](https://mmzztt.com/photo/top/)  
  
# Miscellaneous
Selenium is not used as a middleware but directly coded in the spider