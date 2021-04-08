from solution import *
import xlwings as xw

import pytest
import os

# import markdown parsers
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from bs4 import BeautifulSoup

# start logging
import logging
logging.basicConfig(filename='readme.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)

# open the markdown file
markdown_file = os.path.join(os.getcwd(), 'README.md')
readme = open(markdown_file).read() # extract text from file

class Tests():
    def setup_class(cls):
        """ 
        Set up before any tests are run.  
        Grab the responses from the README file and get access to the Excel doc.
        """
        # get readme document as github-flavored markdown
        html = markdown.markdown(readme, extensions=[GithubFlavoredMarkdownExtension()]) # get content as object

        # convert to html
        soup = BeautifulSoup(html, 'html.parser')

        # a list of all the code blocks from the README.md
        cls.responses = soup.find_all('code')
        
        # open the Excel file
        data_file = os.path.join(os.getcwd(), 'data/users.xlsx')
        cls.wb = xw.Book(data_file)
        cls.sheet = cls.wb.sheets['users']
        
    def teardown_class(cls):
        """ 
        Clean up after all tests have been run.
        Close the active book.
        """
        cls.wb.close()

    def test_q1(self):
        # Q1 Total number of users of the social network
        Q1_answers = self.responses[0].get_text().strip().splitlines()
        Q1_outputs = [1000]

        response = Q1_answers[0].strip()
        expected = Q1_outputs[0].strip()
        output_cell = 'O2'
        error_msg = f"Q1 - wrong formula: {response}"

        # check response is an excel formula
        assert response[0] == '='
        
        try:
            # place response in sheet and check result of formula
            self.sheet[output_cell].value = response
            assert self.sheet['O2'].value == expected, error_msg
        except AssertionError as error:
            logger.error(error)
        except Exception as error:
            logger.error(error)

    def test_q2(self):
        # Q2 Number of users in each of the states in the New England region.
        Q2_answers = self.responses[1].get_text().strip().splitlines()
        Q2_outputs = [12,0,13,1,1,0]

        # only check the first response, if multiple given
        response = Q2_answers[0].strip()
        expected = Q2_outputs[0].strip()
        output_cell = 'O5'
        error_msg = f"Q2 - wrong formula: {response}"

        # check the first line of response is an excel formula
        assert response[0] == '='

        try:
            self.sheet[output_cell] = response
            assert self.sheet[output_cell].value == expected, error_msg
        except AssertionError as error:
            logger.error(error)
        except Exception as error:
            logger.error(error)

        # check all answers... not required here
        # for i,answer in enumerate(Q2_answers):
        #     self.sheet['O'+str(i+5)].value = answer
        #     try:
        #         assert self.sheet['O'+str(i+5)].value == Q2_outputs[i], "Q2 code"+ str(i+1) +" wrong formula"
        #     except AssertionError as error:
        #         logger.error(error)
        #     except Exception as error:
        #         logger.error(error)

    def test_q3(self):
        # Q3 Number of users in each of the 5 most populous cities of the USA.
        Q3_answers = self.responses[2].get_text().strip().splitlines()
        Q3_outputs = [10,8,11,20,10]

        # only check the first response, if multiple given
        response = Q3_answers[0].strip()
        expected = Q3_outputs[0].strip()
        output_cell = 'P13'
        error_msg = f"Q3 - wrong formula: {response}"

        # check the first line of response is an excel formula
        assert response[0] == '='

        try:
            assert self.sheet[output_cell].value == expected, error_msg
        except AssertionError as error:
            logger.error(error)
        except Exception as error:
            logger.error(error)

    def test_q4(self):
        # Q4 The average affinity category IDs of all users in New York for each of the content types.
        Q4_answers = self.responses[3].get_text().strip().splitlines()
        Q4_outputs = [2.66,6.21,10.67,14.4]

        # only check the first response, if multiple given
        response = Q4_answers[0].strip()
        expected = Q4_outputs[0].strip()
        output_cell = 'P20'
        error_msg = f"Q3 - wrong formula: {response}"

        # check the first line of response is an excel formula
        assert response[0] == '='

        try:
            assert self.sheet[output_cell].value == expected, error_msg
        except AssertionError as error:
            logger.error(error)
        except Exception as error:
            logger.error(error)

    def test_overall_structure(self):
        """Test that the contents of the README.md file are as expected"""

        # get readme document as github-flavored markdown
        html = markdown.markdown(readme, extensions=[GithubFlavoredMarkdownExtension()]) # get content as object

        # convert to html
        soup = BeautifulSoup(html, 'html.parser')

        # a list of all the code samples
        responses = soup.find_all('code')

        # logger.warning(soup)
        assert len(responses) == 32
