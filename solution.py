# write your Python code here according to the instructions

## import the csv module
import csv

def get_csv_data(filepath):
    """
    Opens the file at filepath, reads the data using the csv module's DictReader, 
    converts that data to a regular list and returns that list.

    :param filepath: The file path of the CSV data file to open
    :returns: A list of dictionaries, where each dictionary represents one row from the file
    """

def remove_rows_with_blank_fields(data):
    """
    Removes any rows with one or more blank fields from the data set

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above

def remove_rows_in_uk(data):
    """
    Removes any rows with 'United Kingdom' in the 'state' field.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above


def remove_rows_over_one_dollar(data):
    """
    Removes any rows with a value higher than 100 in the 'cost_per_impression' field.

    :param data: The data, as a list of dictionaries
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above


def replace_email_domain(data, old_domain, new_domain):
    """
    Updates any rows where the 'email' ends in the old domain.  Updates to the new domain.

    :param data: The data, as a list of dictionaries
    :param old_domain: The old domain to remove, e.g. '@dmoz.org'
    :param new_domain: The new domain to replace the old_domain with, e.g. '@dmoz.com'
    :returns: The modified data, as a list of dictionaries
    """
    ## place your code here to complete this method according to the instructions above


def save_csv_data(data, filepath):
    """
    Saves the data into the specified file.  Include the field headers as the first row.

    :param data: The data, as a list of dictionaries
    :param filepath: The file path of the CSV data file to save to
    """
    ## place your code here to complete this method according to the instructions above


def get_average_cost_per_impression(filepath):
    """
    Calculates the average cost per impression of all records in the data set.

    :param filepath: The file path of the CSV data file to open
    :returns: The average cost per impression of all records in the data set
    """
    ## place your code here to complete this method according to the instructions above


#################################################
## Do not modify the code below this line      ##
## except to comment out any function calls    ##
## that you do not wish to test at the moment  ##
#################################################

def main():
    ## use the functions defined above to complete munging of the data file

    # get the data from the file
    data = get_csv_data('data/users.csv')
    
    # munge it
    data = remove_rows_with_blank_fields(data)
    data = remove_rows_in_uk(data)
    data = remove_rows_over_one_dollar(data)
    data = replace_email_domain(data, '@dmoz.org', '@dmoz.com')

    # dave to the new csv file
    save_csv_data(data, 'data/users_clean.csv')

    # print the average cost per impression from the data in the file
    avg = get_average_cost_per_impression('data/users_clean.csv')
    print('The average cost per impression is:', format(avg, '.0f'), 'cents') # format number nicely

if __name__ == "__main__":
    main()
