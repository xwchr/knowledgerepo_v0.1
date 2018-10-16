# KnowledgeRepo v0.1
This repository contains the sourcecode for the software that runs the "Tracking the Trackers" online knowledge repository and website (see http://beta.trackingthetracker.net).

(c) Cracked Labs 2018, GNU General Public License 3.0

## About

KnowledgeRepo provides a curated and annotated online research database that makes relevant resources such as news articles, blog posts, academic papers, and policy reports accessible. Similarly to an academic reference database, it contains bibliographic information on publications. Every entry includes a custom short abstract and is manually tagged, both with generic tags and with a second category of tags referring to the companies, brands, products or services mentioned. In contrast to a pure reference management system, the database can be explored through a directory of topics, which are collections of resources on specific issues based on pre-defined searches. Every topic lists one or more sets of relevant publications with certain tags and document attributes. This way, KnowledgeRepo aims to:

* make it easier to enter, understand, overview, and follow the debate on specific issues for journalists, academics, advocacy groups, activists, policymakers, regulators, and others;
* combine information about actual corporate practices with a broader understanding and analysis from multidisciplinary perspectives;
* cumulatively build a knowledge repository that allows to cross-link information between different areas and understand longer-term developments.

## Requirements

KnowledgeRepo is a web application that is based on the python-based `Django` framework and `PostgreSQL`. Document metadata is inspired by `Dublin Core` and `Zotero`. Tagging is based on `django-tagulous` and the topic hierachy is based on `django-mptt`. The current version requires:

* Django 2.0+
* django-mptt 0.9
* django-tagulous 0.13.2+
* django-admin-sortable2 0.6.19+
* django-autocomplete-light 3.2.10+
* django-js-asset 1.1+

To run it in production mode `django-cachalot` and `Memcached` are recommended.

## Further plans and ideas

* Making the database available via web services,
* Making the contents of included publications full-text searchable (challenging with regards to copyright),
* Implementing advanced information retrieval technologies (e.g. automatically extracting company names, concepts, and technologies from documents)
* More automation – while manual curation is a feature, in the medium term it makes sense to add more automation where it fits.
* Currently, publications are not directly offered on the platform, but link to their original places on the web, if available. With regards to copyright it would be possible to directly provide publications that are licensed under Creative Commons BY-SA or compatible licenses. For other documents, we are thinking about whether it might be legally feasible to link to archive.org or archive.is versions.

## Contact

For feedback or more info contact `impact|crackedlabs|org`.