from typing import Tuple, Optional, Union

from requests import Response
from requests.exceptions import HTTPError

import pandas as pd
import numpy as np

from logging import Logger
from redata.commons.logger import log_stdout
from redata.commons.issue_request import redata_request


class FigshareInstituteAdmin:
    """
    A Python interface for administration and data curation
    with institutional Figshare instances

    Most methods take an ``article_id`` or ``curation_id`` input

    :param token: Figshare OAuth2 authentication token
    :param stage: Flag to either use Figshare stage or production API. Default: production
    :param admin_filter: List of filters to remove admin accounts from user list
    :param log: Logger object for stdout and file logging. Default: stdout

    :ivar token: Figshare OAuth2 authentication token
    :ivar stage: Flag to either use Figshare stage or prod API
    :ivar baseurl: Base URL of Figshare API
    :ivar baseurl_institute: Base URL of Figshare API for institutions
    :ivar headers: HTTP header information
    :ivar admin_filter: List of filters to remove admin accounts from user list
    :ivar ignore_admin: Flags whether to remove admin accounts from user list
    """

    def __init__(self, token: str, stage: bool = False,
                 admin_filter: list = None,
                 log: Logger = log_stdout()):

        self.token = token
        self.stage = stage

        if not self.stage:
            self.baseurl = "https://api.figshare.com/v2/account/"
        else:
            self.baseurl = "https://api.figsh.com/v2/account/"

        self.baseurl_institute = self.baseurl + "institution/"

        self.headers = {'Content-Type': 'application/json'}
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

        self.admin_filter = admin_filter
        if admin_filter is not None:
            self.ignore_admin = True
        else:
            self.ignore_admin = False
        self.log = log

    def endpoint(self, link: str, institute: bool = True) -> str:
        """Concatenate the endpoint to the baseurl for ``requests``

        :param link: API endpoint to append to baseurl
        :param institute: Flag to use regular of institute baseurl

        :return: URL for HTTPS API
        """
        if institute:
            return self.baseurl_institute + link
        else:
            return self.baseurl + link

    def get_articles(self, process: bool = True) -> \
            Union[pd.DataFrame, Response]:
        """
        Retrieve information about all articles within institutional instance

        See: https://docs.figshare.com/#private_institution_articles

        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all articles for an institution or
                 the full ``requests.Response``
        """

        url = self.endpoint("articles")

        # Figshare API is limited to a maximum of 1000 per page
        # Full pagination still needed
        params = {'page': 1, 'page_size': 1000}
        articles = redata_request('GET', url, self.headers, params=params,
                                  process=process)

        if process:
            articles_df = pd.DataFrame(articles)
            return articles_df
        else:
            return articles

    def get_user_articles(self, account_id: int, process: bool = True) \
            -> Union[pd.DataFrame, Response]:
        """
        Impersonate a user, ``account_id``, to retrieve articles
        associated with the user.

        See: https://docs.figshare.com/#private_articles_list

        :param account_id: Figshare *institute* account ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all articles owned by user or
                 the full ``requests.Response``
        """

        url = self.endpoint("articles", institute=False)

        # Figshare API is limited to a maximum of 1000 per page
        params = {'page': 1, 'page_size': 1000, 'impersonate': account_id}
        user_articles = redata_request('GET', url, self.headers,
                                       params=params, process=process)

        if process:
            user_articles_df = pd.DataFrame(user_articles)
            return user_articles_df
        else:
            return user_articles

    def get_user_projects(self, account_id: int, process: bool = True) \
            -> Union[pd.DataFrame, Response]:
        """
        Impersonate a user, ``account_id``, to retrieve projects
        associated with the user.

        See: https://docs.figshare.com/#private_projects_list

        :param account_id: Figshare *institute* account ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all projects owned by user or
                 the full ``requests.Response``
        """

        url = self.endpoint("projects", institute=False)

        # Figshare API is limited to a maximum of 1000 per page
        params = {'page': 1, 'page_size': 1000, 'impersonate': account_id}
        user_projects = redata_request('GET', url, self.headers,
                                       params=params, process=process)

        if process:
            user_projects_df = pd.DataFrame(user_projects)
            return user_projects_df
        else:
            return user_projects

    def get_user_collections(self, account_id: int, process: bool = True) \
            -> Union[pd.DataFrame, Response]:
        """
        Impersonate a user, ``account_id``, to retrieve collections
        associated with the user.

        See: https://docs.figshare.com/#private_collections_list

        :param account_id: Figshare *institute* account ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all collections owned by user or
                 the full ``requests.Response``
        """

        url = self.endpoint("collections", institute=False)

        # Figshare API is limited to a maximum of 1000 per page
        params = {'page': 1, 'page_size': 1000, 'impersonate': account_id}
        user_collections = redata_request('GET', url, self.headers,
                                          params=params, process=process)

        if process:
            user_collections_df = pd.DataFrame(user_collections)
            return user_collections_df
        else:
            return user_collections

    def get_groups(self, process: bool = True) -> \
            Union[pd.DataFrame, Response]:
        """
        Retrieve information about groups within institutional instance.

        See: https://docs.figshare.com/#private_institution_groups_list

        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all Figshare groups for an institution
                 or the full ``requests.Response``
        """

        url = self.endpoint("groups")
        groups = redata_request('GET', url, self.headers, process=process)

        if process:
            groups_df = pd.DataFrame(groups)
            return groups_df
        else:
            return groups

    def get_account_list(self, process: bool = True) -> \
            Union[pd.DataFrame, Response]:
        """
        Return pandas DataFrame of user accounts.

        See: https://docs.figshare.com/#private_institution_accounts_list

        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all user accounts for an institution
                 or the full ``requests.Response``
        """

        url = self.endpoint("accounts")

        # Figshare API is limited to a maximum of 1000 per page
        params = {'page': 1, 'page_size': 1000}
        accounts = redata_request('GET', url, self.headers,
                                  params=params, process=process)

        if process:
            accounts_df = pd.DataFrame(accounts)
            accounts_df = accounts_df.drop(columns='institution_id')

            if self.ignore_admin:
                self.log.info("Excluding administrative and test accounts")

                drop_index = []
                for ia in self.admin_filter:
                    drop_index += list(accounts_df[accounts_df['email'].str.contains(ia)].index)

                if len(drop_index) > 0:
                    accounts_df = accounts_df.drop(drop_index).reset_index(drop=True)
            return accounts_df
        else:
            return accounts

    def get_account_group_roles(self, account_id: int, process: bool = True) \
            -> Union[dict, Response]:
        """
        Retrieve group roles for a given account, ``account_id``.

        See: https://docs.figshare.com/#private_institution_account_group_roles

        :param account_id: Figshare *institute* account ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Python dictionary of all group roles for a user or
                 the full ``requests.Response``
        """

        url = self.endpoint(f"roles/{account_id}")

        roles = redata_request('GET', url, self.headers, process=process)
        return roles

    def get_account_details(self, flag: bool = True) -> pd.DataFrame:
        """
        Retrieve account details. This includes group association, number of
        articles, projects, and collections, and administrative and reviewer
        role flags

        :param flag: Populate administrative and reviewer roles to database

        :return: Relational database of details of all accounts for an institution
        """

        # Retrieve accounts
        accounts_df = self.get_account_list()

        n_accounts = accounts_df.shape[0]

        # Retrieve groups
        groups_df = self.get_groups()

        num_articles = np.zeros(n_accounts, dtype=np.intc)
        num_projects = np.zeros(n_accounts, dtype=np.intc)
        num_collections = np.zeros(n_accounts, dtype=np.intc)

        orcid_num = [''] * n_accounts
        user_id = np.zeros(n_accounts, dtype=np.intc)  # This is the Figshare user ID

        if flag:
            admin_flag = [''] * n_accounts
            reviewer_flag = [''] * n_accounts
        group_assoc = ['N/A'] * n_accounts

        # Determine group roles for each account
        for n, account_id in zip(range(n_accounts), accounts_df['id']):
            # Save ORCID and account ID
            other_account_dict = self.get_other_account_details(account_id)
            orcid_num[n] = other_account_dict['orcid_id']
            user_id[n] = other_account_dict['id']

            roles = self.get_account_group_roles(account_id)

            try:
                articles_df = self.get_user_articles(account_id)
                num_articles[n] = articles_df.shape[0]
            except HTTPError:
                self.log.warning(
                    f"Unable to retrieve articles for : {account_id}"
                )

            try:
                projects_df = self.get_user_projects(account_id)
                num_projects[n] = projects_df.shape[0]
            except HTTPError:
                self.log.warning(
                    f"Unable to retrieve projects for : {account_id}"
                )

            try:
                collections_df = self.get_user_collections(account_id)
                num_collections[n] = collections_df.shape[0]
            except HTTPError:
                self.log.warning(
                    f"Unable to retrieve collections for : {account_id}"
                )

            for key in roles.keys():
                for t_dict in roles[key]:
                    if t_dict['id'] == 11:
                        group_assoc[n] = key
                    if flag:
                        if t_dict['id'] == 2:
                            admin_flag[n] = 'X'
                        if t_dict['id'] == 49:
                            reviewer_flag[n] = 'X'

        accounts_df['Articles'] = num_articles
        accounts_df['Projects'] = num_projects
        accounts_df['Collections'] = num_collections

        accounts_df['ORCID'] = orcid_num
        accounts_df['user_id'] = user_id

        if flag:
            accounts_df['Admin'] = admin_flag
            accounts_df['Reviewer'] = reviewer_flag

        for group_id, group_name in zip(groups_df['id'], groups_df['name']):
            self.log.info(f"{group_id} - {group_name}")
            group_assoc = [sub.replace(str(group_id), group_name) for
                           sub in group_assoc]

        accounts_df['Group'] = group_assoc
        return accounts_df

    def get_other_account_details(self, account_id: int) -> dict:
        """
        Retrieve ORCID and Figshare account information (among other metadata)

        See: https://docs.figshare.com/#private_account_institution_user

        :param account_id: Figshare *institute* account ID

        :return: Dictionary with full account details
        """

        url = self.endpoint(f"users/{account_id}", institute=True)

        other_account_dict = redata_request('GET', url, self.headers)

        return other_account_dict

    def get_curation_list(self, article_id: int = None,
                          status: Optional[str] = "", process: bool = True) \
            -> Union[pd.DataFrame, Response]:
        """
        Retrieve list of curation records for ``article_id``.
        If not specified, all curation records are retrieved.

        See: https://docs.figshare.com/#account_institution_curations

        :param article_id: Figshare article ID
        :param status: Filter by status of review. Options are:
               ['', 'pending', 'approved', 'rejected', 'closed']
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Relational database of all curation records or
                 the full ``requests.Response``
        """
        status_list = ['', 'pending', 'approved', 'rejected', 'closed']
        if status not in status_list:
            raise ValueError(f"Incorrect status input. Most be one of {status_list}")

        url = self.endpoint("reviews")

        params = {'offset': 0, 'limit': 1000}
        if article_id is not None:
            params['article_id'] = article_id

        if status:
            params['status'] = status

        curation_list = redata_request('GET', url, self.headers,
                                       params=params, process=process)

        if process:
            curation_df = pd.DataFrame(curation_list)
            return curation_df
        else:
            return curation_list

    def get_curation_details(self, curation_id: int, process: bool = True) \
            -> Union[dict, Response]:
        """
        Retrieve details about a specified curation, ``curation_id``.

        See: https://docs.figshare.com/#account_institution_curation

        :param curation_id: Figshare curation ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Python dictionary with curation metadata or
                 the full ``requests.Response``
        """

        url = self.endpoint(f"review/{curation_id}")

        curation_details = redata_request('GET', url, self.headers,
                                          process=process)
        return curation_details

    def get_curation_comments(self, curation_id: int, process: bool = True) \
            -> Union[dict, Response]:
        """
        Retrieve comments about specified curation, ``curation_id``.

        See: https://docs.figshare.com/#account_institution_curation_comments

        :param curation_id: Figshare curation ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Python dictionary with curation comments or
                 the full ``requests.Response``
        """

        url = self.endpoint(f"review/{curation_id}/comments")

        curation_comments = redata_request('GET', url, self.headers,
                                           process=process)
        return curation_comments

    def doi_check(self, article_id: int, process: bool = True) -> \
            Union[Tuple[bool, str], Response]:
        """
        Check if DOI is present/reserved for ``article_id``.

        Uses: https://docs.figshare.com/#private_article_details

        :param article_id: Figshare article ID
        :param process: Returns JSON content from ``redata_request``, otherwise
                        the full request is provided. Default: True

        :return: Flag to indicate whether DOI is reserved and DOI (empty string if not).
                 Returns the full ``requests.Response`` if ``process=False``
        """
        url = self.endpoint(f"articles/{article_id}", institute=False)

        article_details = redata_request('GET', url, self.headers,
                                         process=process)

        if process:
            check = False
            if article_details['doi']:
                check = True

            return check, article_details['doi']
        else:
            return article_details

    def reserve_doi(self, article_id: int) -> str:
        """
        Reserve DOI if one has not been reserved for ``article_id``.

        See: https://docs.figshare.com/#private_article_reserve_doi

        :param article_id: Figshare article ID

        :return: DOI string
        """

        url = self.endpoint(f"articles/{article_id}/reserve_doi",
                            institute=False)

        # Check if DOI has been reserved
        doi_check, doi_string = self.doi_check(article_id)

        if doi_check:
            self.log.info("DOI already reserved! Skipping... ")
            return doi_string
        else:
            self.log.info(
                "PROMPT: DOI reservation has not occurred! Do you wish to reserve?"
            )
            src_input = input(
                "PROMPT: Type 'Yes'/'yes'. Anything else will skip : "
            )
            self.log.info(f"RESPONSE: {src_input}")
            if src_input.lower() == 'yes':
                self.log.info("Reserving DOI ... ")
                response = redata_request('POST', url, self.headers)
                self.log.info(f"DOI minted : {response['doi']}")
                return response['doi']
            else:
                self.log.warning("Skipping... ")
                return doi_string
