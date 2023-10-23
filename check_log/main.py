import os

# path to files
LOGS_FILE = '/var/log/asterisk/full'
REPORT_FILE = '/home/report.txt'
# events
EVENT = ''

# email
EMAIL = ''


def open_file(path):
    file = open(path, 'r')
    logs = file.readlines()
    return logs


def check_report_file():
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'x'):
            pass


def main():
    check_report_file()
    logs = open_file(LOGS_FILE)
    reports = open_file(REPORT_FILE)
    report_file = open(REPORT_FILE, 'a')
    found = ''
    for elem in logs:
        if EVENT in elem:
            if elem not in reports:
                report_file.writelines(elem)
                found = found + f'{elem}'
    report_file.close()
    if found != '':
        os.system(f'mail -s "105" {EMAIL} <<< "{found}"')


if __name__ == '__main__':
    main()
