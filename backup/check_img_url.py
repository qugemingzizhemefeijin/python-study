import requests
import sys


def is_valid_image_url(url):
    try:
        response = requests.get(url, stream=True, timeout=5)
        content_type = response.headers.get('Content-Type', '')
        status_code = response.status_code
        if status_code == 200 and content_type.startswith('image/'):
            return True
        else:
            return False
    except requests.RequestException:
        return False


def check_urls(input_file, output_file='C:/aaa.txt'):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            url = line.strip()
            if not url:
                continue
            print(f"Checking: {url}")
            if is_valid_image_url(url):
                print("✅ Valid image")
            else:
                print("❌ Invalid image")
                outfile.write(url + '\n')
            print('------------------------')


if __name__ == "__main__":
    check_urls('C:/bbb.txt')
