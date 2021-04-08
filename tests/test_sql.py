import os
import pytest
import sqlite3

# import markdown parsers
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from bs4 import BeautifulSoup

# start logging
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# expected SQL queries (please verify if they are correct)
SQL_QUERY_3 = 'SELECT state,count(ID) as numUsers FROM users WHERE state!="" GROUP BY state;'
SQL_QUERY_4 = 'SELECT state,count(ID) as numUsers, avg(real_food_affinity_category_id) FROM users WHERE state!="" GROUP BY state;'
SQL_QUERY_5 = 'SELECT email FROM users WHERE state="Oklahoma" and city="Oklahoma City";'
SQL_QUERY_6 = 'SELECT email, cost_per_impression FROM users INNER JOIN affinity_categories ON users.real_food_affinity_category_id=affinity_categories.id WHERE users.state="Oklahoma" and users.city="Oklahoma City";'
SQL_QUERY_7 = 'SELECT 2*cost_per_thousand FROM affinity_categories WHERE type="real_food_affinity" and level=0.5;'
SQL_QUERY_8 = 'SELECT users.handle from users LEFT JOIN affinity_categories on users.luxury_brand_affinity_category_id = affinity_categories.id WHERE affinity_categories.id is NULL;'

# open the markdown file
readme = open('README.md').read() # extract text from file
test_db_filename = "test_readme.db" # a test database name

class Tests():

    @classmethod
    def get_sql_codes(cls, readme_content):
        """
        Parses the readme file and returns the sql code blocks from the readme
        :param readme_content: content of the readme file
        :return:
        new_codes: SQL code blocks from the readme file
        """
        html = markdown.markdown(readme, extensions=[GithubFlavoredMarkdownExtension()]) # get content as object
        # Currently considering the just SQL queries portion
        html = '\n'.join(html.split("SQL queries")[1:]).split("Normalization and")[0] # grab just the sql commands from the file
        soup = BeautifulSoup(html, 'html.parser')
        codes = soup.find_all('code')
        codes = [c.get_text().strip() for c in codes] # get just inner text

        # clean up the codes
        codes_clean = []
        for code in codes:
            # remove comments
            if '#' in code:
                code = code[ : code.find('#')]
            # remove extra whitespace
            code = code.strip() 
            # skip any blank codes
            if len(code) == 0:
                continue
            # remove accidental semi-colons from dot commands
            if code.startswith('.') and code.endswith(';'):
                code = code[ : code.find(';')]
            # add on missing semi-colons
            if not code.startswith('.') and not code.endswith(';'):
                code = f"{code};"

            # add to new list
            codes_clean.append(code)

        return codes_clean

    @classmethod
    def get_expected_query_output(cls, query):
        """
        Runs the given query in sqlite and returns the output rows
        :param query: SQL query
        :return:
        expected_query_output: Output of running the given SQL query
        """
        cursor = cls.student_db_conn.execute(query)
        expected_query_output = []
        for row in cursor:
            expected_query_output.append(row)
        return expected_query_output

    def setup_class(cls):
        """ 
        Set up before any tests are run.  
        Set up a test database and grab the user's queries to prepare to run them.
        """

        cls.sql_codes = cls.get_sql_codes(readme)
        cls.sql_codes_gen = (x for x in cls.sql_codes) # generator object for getting sql code blocks
        db_data_path = os.path.join(os.getcwd(), "data")
        test_db_filepath = os.path.join(os.getcwd(), "data", test_db_filename)
        db_data_filepath = os.path.join(os.getcwd(), "data", [x for x in os.listdir(db_data_path) if ".db" in x][0])
        cls.test_db_conn = sqlite3.connect(test_db_filepath) # making a new test sqlite db to test the first two queries in exam
        cls.student_db_conn = sqlite3.connect(db_data_filepath) # using the db file of student to run the other queries

    def teardown_class(cls):
        """
        Clean up after all tests have completed.
        Remove the test db file.
        """
        test_db_filepath = os.path.join(os.getcwd(), "data", test_db_filename)
        if os.path.exists(test_db_filepath):
            os.remove(test_db_filepath)

    def test_sql_queries_length(self):
        assert len(self.sql_codes) == 11

    def test_sql_query_1_1(self):
        try:
            self.test_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False

    def test_sql_query_1_2(self):
        try:
            self.test_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False

    def test_sql_query_2_1(self):
        try:
            command = next(self.sql_codes_gen)
            # command = command.replace(". ", ".")
            self.test_db_conn.execute(command)
        except Exception as ex:
            logger.error(ex)
            assert False

    def test_sql_query_2_2(self):
        try:
            command = next(self.sql_codes_gen)
            # command = command.replace(". ", ".")
            self.test_db_conn.execute(command)
        except Exception as ex:
            logger.error(ex)
            assert False

    def test_sql_query_3(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_3_output = self.get_expected_query_output(SQL_QUERY_3)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_3_output)
        assert set(student_query_output) == set(expected_query_3_output)

    def test_sql_query_4(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_4_output = self.get_expected_query_output(SQL_QUERY_4)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_4_output)
        assert set(student_query_output) == set(expected_query_4_output)

    def test_sql_query_5(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_5_output = self.get_expected_query_output(SQL_QUERY_5)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_5_output)
        assert set(student_query_output) == set(expected_query_5_output)

    def test_sql_query_6(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_6_output = self.get_expected_query_output(SQL_QUERY_6)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_6_output)
        assert set(student_query_output) == set(expected_query_6_output)

    def test_sql_query_7(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_7_output = self.get_expected_query_output(SQL_QUERY_7)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_7_output)
        assert set(student_query_output) == set(expected_query_7_output)

    def test_sql_query_8(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
        
        expected_query_8_output = self.get_expected_query_output(SQL_QUERY_8)
        student_query_output = []
        for row in cursor:
            student_query_output.append(row)
        
        assert len(student_query_output) == len(expected_query_8_output)
        assert set(student_query_output) == set(expected_query_8_output)

    def test_sql_query_9(self):
        try:
            cursor = self.student_db_conn.execute(next(self.sql_codes_gen))
        except Exception as ex:
            logger.error(ex)
            assert False
