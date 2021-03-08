import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://www.legatbogen.dk/horsens-kommune/stoetteomraade/20558'


class LegatbogenPage:
    def __init__(self, link):
        self.link = link
        r = requests.get(link)
        self.html_content = BeautifulSoup(r.content, 'html.parser')

    @staticmethod
    def _clean_output(word):
        word = str(word)
        return re.sub('<[^>]+>', '', word)

    def get_data(self):
        # Instantiate everything to start with as there are many missing values
        firm_name = []
        grant_name = []
        grant_id = [str(self.link.split('/')[-1])]
        avg_amount = []
        portions = []
        apply_open = []
        apply_before = []
        answer_date = []
        payout_date = []
        list_supported = []
        list_not_supported = []
        documentation_requirements = []
        link = [self.link]
        application_method = []

        cols = ['Link', 'Grant id', 'Firm name', 'Grant name', 'Avg annual amount', 'Portion size', 'Apply before',
                'Apply open', 'Response date', 'Payout date', 'Documentation required', 'Supported',
                'Not supported', 'Application method']

        # Edgecase handling
        try:
            if str(self.html_content.find_all("span", {"class": "headline_donation_text_closed h4"})[0].contents[
                       0]) == 'Ophørt':
                d = pd.DataFrame(list(
                    zip(['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'],
                        ['Ophørt'],
                        ['Ophørt'],
                        ['Ophørt'], ['Ophørt'], ['Ophørt'], ['Ophørt'])))

                d.columns = cols
                return d
        except IndexError:
            pass

        temp_avg_spend = str(
            self.html_content.find_all("span", {"class": "headline_donation_text_value h4 h4-base"})[0].contents[0])
        avg_amount.append(self._clean_output(temp_avg_spend))

        firm_name.append(str(self.html_content.find_all("h2", {"class": "headline_title"})[0].contents[0]))

        temp_grant_name = self.html_content.find_all("h1", {"class": "foundationGrant_main_header_headline h1 h1-base"})
        grant_name.append(
            str([i.contents[0].contents[0] + ' ' + i.contents[2].contents[0] for i in temp_grant_name][0]))

        temp_portions = \
            self.html_content.find_all("div", {"class": "foundationGrantSummary_section_text_value h4 h4-base"})[
                0].contents[0]
        portions.append(self._clean_output(temp_portions))

        deadline = self.html_content.find_all("div", {"class": "foundationGrantDates_period_row_text"})

        try:
            apply_open.append(deadline[0].contents[0])
        except IndexError:
            apply_open.append('Error')
        try:
            apply_before.append(deadline[1].contents[0])
        except IndexError:
            apply_before.append('Error')
        try:
            answer_date.append(deadline[2].contents[0])
        except IndexError:
            answer_date.append('Error')
        try:
            payout_date.append(deadline[3].contents[0])
        except IndexError:
            payout_date.append('Error')

        # Qualitative statements
        supported = self.html_content.find_all("div", {
            "class": "foundationGrantPurpose_list foundationGrantPurpose_list-supported"})
        temp_list_supported = ''

        for i in supported:
            temp_supported = i.find_all("li", {"class": "foundationGrantPurpose_list_element"})
            for i in temp_supported:
                temp_list_supported += self._clean_output(i.contents[0])
                temp_list_supported += '\n'

        list_supported.append(temp_list_supported)

        not_supported = self.html_content.find_all("div", {
            "class": "foundationGrantPurpose_list foundationGrantPurpose_list-notSupported"})
        temp_list_not_supported = ''

        for i in not_supported:
            temp_not_supported = i.find_all("li", {"class": "foundationGrantPurpose_list_element"})
            for i in temp_not_supported:
                temp_list_not_supported += self._clean_output(i.contents[0])
                temp_list_not_supported += '\n'

        list_not_supported.append(temp_list_not_supported)

        documents = self.html_content.find_all("div", {"class": "foundationGrantApplyDocument_name"})
        documentation_requirements.append(''.join(x.contents[0] + '\n' for x in documents))

        try:
            temp_app_method = self.html_content.find_all("div", {"class": "foundationGrantApply_method_inner"})
            application_method.append(self._clean_output(temp_app_method[0]))
        except IndexError:
            application_method.append('Error')
            pass

        d = pd.DataFrame(list(
            zip(link, grant_id, firm_name, grant_name, avg_amount, portions, apply_before, apply_open, answer_date,
                payout_date, documentation_requirements, list_supported, list_not_supported, application_method)))

        d.columns = cols
        return d


if __name__ == '__main__':
    page = LegatbogenPage(url)
    print(page.get_data())
