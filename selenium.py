import sys
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#-----------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Test the ability of the reg application to '
            + 'handle "primary" queries')

    parser.add_argument(
        'serverURL', metavar='serverURL', type=str,
        help='the URL of the application')

    parser.add_argument(
        'browser', metavar='browser', type=str,
        choices=['firefox', 'chrome'],
        help='the browser (firefox or chrome) that you want to use')

    parser.add_argument(
        'mode', metavar='mode', type=str,
        choices=['normal','headless'],
        help='the mode (normal or headless) that this program should '
            + 'use when interacting with Firefox; headless tells '
            + 'the browser not to display its window and so is faster, '
            + 'especially when using X Windows')

    parser.add_argument(
        'delay', metavar='delay', type=int,
        help='the number of seconds that this program should delay '
            + 'between interactions with the browser')

    args = parser.parse_args()

    return (args.serverURL, args.browser, args.mode, args.delay)

#-----------------------------------------------------------------------

def create_driver(browser, mode):

    if browser == 'firefox':
        from selenium.webdriver.firefox.options import Options
        try:
            options = Options()
            if mode == 'headless':
               options.add_argument('-headless')
            driver = webdriver.Firefox(options=options)
        except Exception as ex:  # required if using snap firefox
            from selenium.webdriver.firefox.service import Service
            options = Options()
            if mode == 'headless':
                options.add_argument('-headless')
            service = Service(executable_path='/snap/bin/geckodriver')
            driver = webdriver.Firefox(options=options, service=service)

    else:  # browser == 'chrome'
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if mode == 'headless':
            options.add_argument('-headless')
        options.add_argument('--remote-debugging-pipe')
        driver = webdriver.Chrome(options=options)

    return driver

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_pantry_test(delay, driver, pantry):
    try:
        search_input = driver.find_element(By.ID, 'SearchBox')
        search_input.send_keys(pantry)
        time.sleep(delay) # Necessary for virtual DOM libraries.
        
        time.sleep(delay)

        overviews_table = driver.find_element(By.ID, 'pantry-table')
        print_flush(overviews_table.text)

    except Exception as ex:
        print(str(ex), file=sys.stderr)

#-----------------------------------------------------------------------

def main():
    
    server_url = "https://localhost:5000/pantry?"
    browser = "chrome"
    mode = "normal"
    delay = 3

    driver = create_driver(browser, mode)

    driver.get(server_url)

    # Given Tests
    run_pantry_test(delay, driver,"egg")

    driver.quit()

if __name__ == '__main__':
    main()