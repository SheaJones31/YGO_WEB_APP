import requests
import config


def main(data_storage_file):
    response = requests.get(config.API_URL, verify=False)
    with open(data_storage_file, 'w') as f:
        f.write(response.text)


if __name__ == '__main__':
    main(data_storage_file='response.txt')
