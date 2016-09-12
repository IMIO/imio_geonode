Changelog
=========

0.2.13 (unreleased)
-------------------

- Modify ESRI identify parameters.


0.2.12 (2016-06-22)
-------------------

- Fix for POST Survey


0.2.11 (2016-06-22)
-------------------

- Remove CSRF check for POST Survey queries and add tests.


0.2.10 (2016-04-20)
-------------------

- Improve tests
- Result for each layer contain new attributes :
  success : True or False -> Indicate the success of the Query
  message : Non-empty if failure to query a layer


0.2.9 (2016-04-20)
------------------

- ESRI querier query hidden layers (all parameters)
- ESRI querier layer can be limited to specifics layers
- Added description for layer

0.2.8 (2016-04-20)
------------------

- More precise ESRI identify queries
- Improve admin configuration lisibility


0.2.7 (2016-04-20)
------------------

- Esri queries now support Multipolygon (experimental)


0.2.6 (2016-04-18)
------------------

- Change WFS queries form 1.0.0 to 1.1.0 (for Liege)


0.2.5 (2016-03-22)
------------------

- Add WFS querier to imio_survey


0.2.4 (2016-01-13)
------------------

- Add first version of imio_survey


0.2.3 (2015-12-15)
------------------

- Remove layer_title from WMC


0.2.2 (2015-12-15)
------------------

- fix and tune map wmc for urbanmap
  [ndufrane]


0.2.1 (2015-11-26)
------------------

- Fix for (bad esri) remote multisource.
  [ndufrane]


0.2 (2015-11-23)
----------------

- Update to geonode 2.4
  [bsuttor]


0.1 (2015-11-20)
-----------------
- initial release
