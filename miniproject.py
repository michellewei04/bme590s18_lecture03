from glob import glob
import os
import pandas as pd
import re

def main():
    collect_all_csv_filenames()
    read_csv()
    write_data()


def collect_all_csv_filenames():
    os.remove('everyone.csv')
    person = []
    allfiles = glob('*.csv')
    for file in allfiles:
        if file != 'mlp6.csv':
            df = pd.read_csv(file, delimiter=',', index_col=None, header=None)
            person.append(df)
    everyone = pd.concat(person, ignore_index=True)
    counter = 0
    for row in everyone[0]:
        if row.isalnum() == 0:
            everyone.drop(everyone.index[counter], inplace=True)
            break
        else:
            counter += 1
    everyone.to_csv('everyone.csv', index=False, header=['Firstname','Lastname','NetID','Githubname','Teamname'])
    # print(everyone)
    pass


def read_csv():
    check_no_spaces()
    check_camel_case()
    pass


def write_data(type='json'):
    # os.remove(glob('*.json'))
    # person = []
    allcsvfiles = glob('*.csv')
    for csvfile in allcsvfiles:
        if csvfile != 'everyone.csv':
            filename = os.path.splitext(csvfile)[0]
            jsonfile = filename + '.json'

            df = pd.read_csv(csvfile, delimiter=',', index_col=None, header=None)
            print(df)
            df.to_json(jsonfile, orient='records')

    pass


def check_no_spaces():
    read_everyone = pd.read_csv('everyone.csv', header=0, index_col=0, engine='python')
    for row in read_everyone['Teamname']:
        row = row.strip()
        if ' ' in row:
            print("Team name %s has spaces" % row)
    pass


def check_camel_case():
    read_everyone = pd.read_csv('everyone.csv', header=0, index_col=0, engine='python')
    p = re.compile('[a-z][A-Z]+')
    camel_teams = []
    for row in read_everyone['Teamname']:
        row = row.strip()
        m = re.search(p, row)
        if m!=None:
            camel_teams.append(row)
    unique_teams = len(set(camel_teams))
    print('Number of unique CamelCases found: {}'.format(unique_teams), flush=True)
    pass
    

if __name__ == "__main__":
    main()
