Changelog
=========

0.2.30 (unreleased)
-------------------

- Nothing changed yet.


0.2.29 (2017-06-12)
-------------------

- Add no-input to syncdb
- Add logging


0.2.28 (2017-03-28)
-------------------

- Optimisation for ESRI Based survey. Using ESRI API Query instead of identify as much as possible


0.2.27 (2017-03-21)
-------------------

- Allow  unchecked POST request for surveyvalues


0.2.26 (2017-03-21)
-------------------

- Add support for DGO4 Old ESRI rest api
- Add LiegeWKT test data
- Add POST facadate for querying values
- Passing POST queries to ESRI API

0.2.25 (2017-03-07)
-------------------

- Pinning setuptools. Workaround requirements madness qith python cffi


0.2.24 (2017-03-07)
-------------------

- Add (optional) area filter to survey_type_list .


0.2.23 (2017-03-06)
-------------------

- Multiple values for distinct.


0.2.22 (2017-01-23)
-------------------

- Add surver_layer_fields for esri layers. Get fields definition for a given layer


0.2.21 (2017-01-10)
-------------------

- Modify survey/survey_type_layers to give layer id instead of layer name


0.2.20 (2016-12-21)
-------------------

- Add survey/survey_type_layers and survey/survey_value_list first version


0.2.19 (2016-12-06)
-------------------

- Pinned urllib3 to 1.19.1


0.2.18 (2016-12-06)
-------------------

- Added urllib3 HTTP client package


0.2.17 (2016-12-06)
-------------------

- Pin celery and django-celery version as celery 4.0.0 does nos support django<1.8


0.2.16 (2016-09-14)
-------------------

- Better WFS Handling
- Better error handling
- Update child lib for POST identify request (esri)
- Set limit for celery chords
- Add layer id in the response


0.2.15 (2016-09-12)
-------------------

- Modification du WFS 1.1.1 querier pour ONE-SPATIAL.


0.2.14 (2016-09-12)
-------------------

- Nothing changed yet.


0.2.13 (2016-09-12)
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
