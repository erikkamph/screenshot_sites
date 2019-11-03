import argparse
from selenium import webdriver
import os


class Capture:
    def __init__(self, browser):
        self.browser = browser
        self.options, self.profile = self.__options__()
        self.driver = self.__driver__()

    def __options__(self):
        options = None
        profile = None
        if self.browser in ("Firefox", "firefox"):
            options = webdriver.FirefoxOptions()
            profile = webdriver.FirefoxProfile()
            profile.set_preference("browser.privatebrowsing.autostart", True)
        elif self.browser in ("Chrome", "chrome"):
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
        else:
            print("Not a valid browser")
            parser.print_usage()
            exit(0)
        options.headless = True
        return options, profile

    def __driver__(self):
        driver = None
        if self.browser in ("Firefox", "firefox"):
            driver = webdriver.Firefox(options=self.options, firefox_profile=self.profile)
        elif self.browser in ("Chrome", "chrome"):
            driver = webdriver.Chrome(options=self.options)
        driver.implicitly_wait(2)
        driver.maximize_window()
        return driver

    def __test_driver__(self):
        if self.driver is None:
            return False
        else:
            return True

    def __loop__(self, in_list):
        with open(in_list, "r") as file:
            lines = file.readlines()
            for l in lines:
                self.__save__(l)

    def __save__(self, addr):
        self.driver.get(addr)
        while self.driver.execute_script("return document.readyState") != "complete":
            continue
        filename = get_filename(addr)
        path = get_path(folder)
        full_path = path + "/" + filename
        self.driver.save_screenshot(full_path)


def get_filename(address):
    name = str(address)
    file = name.replace(":", ".").replace("/", "-")
    file = file + ".png"
    return file


def get_path(var):
    return os.path.expanduser(var)


def main(net):
    capturer = Capture(net)
    if capturer.__test_driver__() is False:
        print("You have to use a valid browser")
        parser.print_usage()
        exit(0)
    if url is not None:
        capturer.__save__(url)
    if iL is not None:
        capturer.__loop__(iL)
    capturer.driver.quit()


if __name__ == "__main__":
    rows, columns = os.popen("stty size", "r").read().split()
    parser = argparse.ArgumentParser(description="A script to take screenshots of websites with either firefox or "
                                                 "chrome", prog="Screenshot")
    parser.add_argument("-v", "--verbose", dest="verbose", help="Print more output when running the program",
                        action="store_true")
    parser.add_argument("-s", "--start", dest="start_at", help="Start on the nth line in the file", default="0",
                        metavar="number")
    parser.add_argument("-iL", "--input-list", dest="input_list", help="What list should the program work its way "
                                                                       "through?", metavar="file")
    parser.add_argument("-i", "--input", dest="input", help="Or better yet what single item should it take a "
                                                            "picture of?", metavar="url")
    parser.add_argument("-b", "--browser", dest="browser", help="Which browser are you planning on using? Chrome or "
                                                                "Firefox?", metavar="browser")
    parser.add_argument("-sD", "--store", dest="folder", help="A path to where you want to store the resulting file(s) "
                                                              "can be relative does not need to be absolute",
                        metavar="folder")
    parser.add_argument("--version", action="version", version='%(prog)s 1.0')
    args = parser.parse_args()
    v = args.verbose
    iL = args.input_list
    url = args.input
    start_pos = args.start_at
    b = args.browser

    folder = ""
    if args.folder is None:
        folder = "~"
    else:
        folder = args.folder

    if b is None:
        print("A browser has to be of either Firefox or Chrome")
        parser.print_usage()
        exit(0)

    if url is None and iL is None:
        print("One of the arguments -iL or -i are required.")
        parser.print_usage()
        exit(0)

    main(args.browser)
