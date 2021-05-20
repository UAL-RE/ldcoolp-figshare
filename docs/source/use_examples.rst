Use Examples
------------

The primary class/object that is used for all interactions with the Figshare API is
:doc:`FigshareInstituteAdmin </ldcoolp_figshare>`. Below are for how to use
this API:

.. code-block:: python

    from ldcoolp_figshare import FigshareInstituteAdmin

    token = "***ENTER YOUR API KEY ***"
    stage = False  # Set to False (True) for production (stage) instance

    fs_admin = FigshareInstituteAdmin(token=token, stage=stage)


There are several methods available with ``FigshareInstituteAdmin``.
We refer users to the full API documentation for more details.
Below we provide some examples to get users started.

Get a list of accounts
~~~~~~~~~~~~~~~~~~~~~~
To retrieve a list of accounts for an institution:

.. code-block:: python

    fs_admin.get_account_list()

Note that this provides you with the ``account_id`` of a user


Obtain curation records
~~~~~~~~~~~~~~~~~~~~~~~
To retrieve a full list of curation records (of any state) for an institution:

.. code-block:: python

    curation_df = fs_admin.get_curation_list()

If you wish to retrieve all curation records for a specific item/deposit,
then provide the ``article_id``:

.. code-block:: python

    article_id = 12345678
    article_curation_df = fs_admin.get_curation_list(article_id)


To obtain more information about a specific curation record:

.. code-block:: python

    curation_id = 1234567
    details_dict = fs_admin.get_curation_details(curation_id)


DOI status and reservation
~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if a DOI is reserved for an item/deposit:

.. code-block:: python

    article_id = 12345678
    check, DOI_string = fs_admin.doi_check(article_id)


Here, ``check`` will either be ``False`` (no DOI) or ``True``.

Alternatively, you can reserve a DOI if it hasn't been done so.
This will provide an prompt before performing the task.
**Note: This step is irreversible!**

.. code-block:: python

    article_id = 12345678
    check, DOI_string = fs_admin.reserve_doi(article_id)


Retrieve list of institution groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    group_df = fs_admin.get_groups()



Retrieve list of articles for a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    account_id = 98765432
    article_df = fs_admin.get_user_articles(account_id)
