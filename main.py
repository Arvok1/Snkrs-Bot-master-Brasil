import os
import sys
import six
import pause
import argparse
import logging.config
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver import Opera
from fake_useragent import UserAgent
import time
from selenium.webdriver.chrome.options import Options
import random
import undetected_chromedriver as uc



logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

NIKE_HOME_URL = "https://www.nike.com.br/"
LOGGER = logging.getLogger()
'width = random.randint(800,1800)
'height = random.randint(800,1800)



def run(driver, username, password, url, shoe_size, deliver_type, login_time=None, release_time=None,
        page_load_timeout=1, screenshot_path=None, html_path=None, select_payment=False, purchase=False,
        num_retries=None):
    set_viewport_size(driver=driver, width=width, height=height)    
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()
    if login_time:
        LOGGER.info("Waiting until login time: " + login_time)
        pause.until(date_parser.parse(login_time))

    try:
        driver.execute_script('return navigator.webdriver')
        login(driver=driver, username=username, password=password)
        driver.save_screenshot('login.png')
    except Exception as e:
        LOGGER.exception("Failed to login: " + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])

    if release_time:
        LOGGER.info("Waiting until release time: " + release_time)
        pause.until(date_parser.parse(release_time))

    num_retries_attempted = 0
    while True:
        try:
            try:
                LOGGER.info("Requesting page: " + url)
                driver.get(url)
            except TimeoutException:
                LOGGER.info("Page load timed out but continuing anyway")

            try:
                select_shoe_size(driver=driver, shoe_size=shoe_size)
                driver.save_screenshot('shoe_size.png')
            except Exception as e:
                # If we fail to select shoe size, try to buy anyway
                LOGGER.exception("Failed to select shoe size: " + str(e))

            try:
                add_to_shopping_cart(driver=driver, deliver_type=deliver_type)
                driver.save_screenshot("shopping_cart.png")
            except Exception as e:
                LOGGER.exception("Failed to click buy button: " + str(e))
                six.reraise(Exception, e, sys.exc_info()[2])

            #try:
            #    go_to_shopping_cart(driver=driver, deliver_type=deliver_type)
            #except Exception as e:
            #    LOGGER.exception("Failed to go to shopping cart: " + str(e))
            #    six.reraise(Exception, e, sys.exc_info()[2])    

            try:
                select_deliver_option(driver=driver, deliver_type=deliver_type)
                driver.save_screenshot("deliver_option.png")
            except Exception as e:
                LOGGER.exception("Failed to select deliver option: " + str(e))
                six.reraise(Exception, e, sys.exc_info()[2])

            try: 
                checkout(driver=driver)
                driver.save_screenshot("checkout.png")
            except Exception as e:
                LOGGER.exception("Failed on checkout: " + str(e))
                six.reraise(Exception, e, sys.exc_info()[2])    


            if select_payment:
                try:
                    select_payment_option(driver=driver)
                except Exception as e:
                    LOGGER.exception("Failed to select payment option: " + str(e))
                    six.reraise(Exception, e, sys.exc_info()[2])

                try:
                    click_save_button(driver=driver)
                except Exception as e:
                    LOGGER.exception("Failed to click save button: " + str(e))
                    six.reraise(Exception, e, sys.exc_info()[2])

            if purchase:
                try:
                    click_submit_button(driver=driver)
                except Exception as e:
                    LOGGER.exception("Failed to click submit button: " + str(e))
                    six.reraise(Exception, e, sys.exc_info()[2])

            LOGGER.info("Purchased shoe")
            break
        except Exception:
            if num_retries and num_retries_attempted < num_retries:
                num_retries_attempted += 1
                LOGGER.info("retrying")
                continue
            else:
                break

    if screenshot_path:
        LOGGER.info("Saving screenshot")
        driver.save_screenshot(screenshot_path)

    if html_path:
        LOGGER.info("Saving HTML source")
        with open(html_path, "w") as f:
            f.write(driver.page_source)

    ##driver.quit()


def login(driver, username, password):
    try:
        LOGGER.info("Requesting page: " + NIKE_HOME_URL)
        driver.get(NIKE_HOME_URL)
    except TimeoutException:
        LOGGER.info("Page load timed out but continuing anyway")

   ## LOGGER.info("Waiting for login button to become clickable")
   ## wait_until_clickable(driver=driver, id="anchor-acessar")
    time.sleep(random.randint(4,20))
    LOGGER.info("Clicking login button")
    wait_until_clickable(driver=driver, id = "anchor-acessar")
    driver.find_element_by_id("anchor-acessar").click()
    time.sleep(random.randint(1,5))

    LOGGER.info("Waiting for login fields to become visible")
    wait_until_visible(driver=driver, xpath="//input[@name='emailAddress']")
    LOGGER.info("Entering username and password")
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(username)
    time.sleep(random.randint(2,10))
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(random.randint(3,10))
    LOGGER.info("Logging in")
    driver.find_element_by_xpath("//input[@value='ENTRAR']").click()
    wait_until_visible(driver=driver, class_name="minha-conta")
    LOGGER.info("Successfully logged in")
    return True

def select_shoe_size(driver, shoe_size):
 ##   LOGGER.info("Waiting for size dropdown button to become clickable")
  ##  wait_until_clickable(driver, class_name="variacoes-tamanhos", duration=10)

 ##   LOGGER.info("Clicking size dropdown button")
 ##   driver.find_element_by_class_name("variacoes-tamanhos").click()
    LOGGER.info("Esperando os tamanhos aparecerem")
    wait_until_visible(driver, xpath=("//label[@for='tamanho__id{shoe_size}']".format(shoe_size=shoe_size)))
    wait_until_clickable(driver, xpath=("//label[@for='tamanho__id{shoe_size}']".format(shoe_size=shoe_size)))
    LOGGER.info("Escolhendo tamanho")
    driver.find_element_by_xpath("//label[@for='tamanho__id{shoe_size}']".format(shoe_size=shoe_size)).click()
    return True 


def add_to_shopping_cart(driver, deliver_type):
##  xpath = "//button[@data-qa='feed-buy-cta']"
    id_ ="btn-comprar"

    LOGGER.info("Esperando o Botão de Adicionar ao carrinho ser clicável")
    wait_until_visible(driver, id=id_)
    wait_until_clickable(driver, id=id_)

    LOGGER.info("Apertando botão de adicionar ao carrinho")
    driver.find_element_by_id(id_).click()
    wait_until_visible(driver, xpath=("//input[@class='form-check-input' and @id='tipo-frete-{deliver_type}']".format(deliver_type=deliver_type)))
    LOGGER.info("Na tela de entrega")

def go_to_shopping_cart(driver, deliver_type):
    driver.get("https://www.nike.com.br/Carrinho")
    wait_until_visible(driver, xpath=("//input[@class='form-check-input' and @id='tipo-frete-{deliver_type}']".format(deliver_type=deliver_type)))
    



def select_deliver_option(driver, deliver_type):
    LOGGER.info("Esperando os fretes aparecerem")
    
    
    wait_until_clickable(driver, xpath=("//input[@class='form-check-input' and @id='tipo-frete-{deliver_type}']".format(deliver_type=deliver_type)))
    LOGGER.info("Escolhendo entrega")
    driver.find_element_by_xpath("//input[@class='form-check-input' and @id='tipo-frete-{deliver_type}]".format(deliver_type=deliver_type)).click()
    

def checkout(driver):
    driver.get("https://www.nike.com.br/Checkout")
    wait_until_clickable(driver, id="seguir-pagamento")
    driver.find_element_by_id("seguir-pagamento").click()
    wait_until_clickable(driver, xpath=("//*[contains(text(), 'Confirmar e Prosseguir')]"))
    driver.find_element_by_xpath("//*[contains(text(), 'Confirmar e Prosseguir')]").click()

def select_payment_option(driver):
    xpath = "//input[@data-qa='payment-radio']"

    LOGGER.info("Waiting for payment checkbox to become clickable")
    wait_until_clickable(driver, xpath=xpath, duration=10)

    LOGGER.info("Checking payment checkbox")
    driver.find_element_by_xpath(xpath).click()


def click_save_button(driver):
    xpath = "//button[text()='Save &amp; Continue']"

    LOGGER.info("Waiting for save button to become clickable")
    wait_until_clickable(driver, xpath=xpath, duration=10)

    LOGGER.info("Clicking save button")
    driver.find_element_by_xpath(xpath).click()


def click_submit_button(driver):
    xpath = "//button[text()='Submit Order']"

    LOGGER.info("Waiting for submit button to become clickable")
    wait_until_clickable(driver, xpath=xpath, duration=10)

    LOGGER.info("Clicking submit button")
    driver.find_element_by_xpath(xpath).click()


def wait_until_clickable(driver, xpath=None, class_name=None, id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    elif id:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, id)))

def wait_until_visible(driver, xpath=None, class_name=None, id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif id:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, id)))

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--shoe-size", required=True)
    parser.add_argument("--login-time", default=None)
    parser.add_argument("--release-time", default=None)
    parser.add_argument("--screenshot-path", default=None)
    parser.add_argument("--html-path", default=None)
    parser.add_argument("--page-load-timeout", type=int, default=30)
    parser.add_argument("--driver-type", default="uc", choices=("firefox", "chrome","opera","uc"))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--select-payment", action="store_true")
    parser.add_argument("--purchase", action="store_true")
    parser.add_argument("--num-retries", type=int, default=1)
    parser.add_argument("--deliver-type", required=True, default=1)
    args = parser.parse_args()

    driver = None
    if args.driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        ua = UserAgent()
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        options.set_preference('permissions.default.stylesheet', 2)
        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        

        if args.headless:
            options.add_argument("--headless")
        if sys.platform == "darwin":
            executable_path = "./bin/geckodriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/geckodriver_linux"
        elif "win32" in sys.platform:
            executable_path ="./bin/geckodriver_win"
        else:
            raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = webdriver.Firefox(executable_path=executable_path, options=options, log_path=os.devnull)


    elif args.driver_type == "chrome":

        options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        print(userAgent)
        ##'geolocation': 2, 'durable_storage': 2, 
        # prefs = {'profile.default_content_setting_values': { 'images': 2,
        #                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
        #                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
         #                   'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
         #                   'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
         #                   'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
         #                   'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'dom.webdriver.enabled': 2, 'useAutomationExtension':2}}
        #options.add_experimental_option('prefs', prefs)
        #options.add_argument("--start-maximized")
        #options.add_argument("--disable-infobars")
        #options.add_argument("--disable-extensions")
        options.add_argument("--incognito")
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("--lang=pt-br")
        options.add_argument("--disable-blink-features=AutomationControlled") #

        if args.headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        if sys.platform == "darwin":
            executable_path = "./bin/chromedriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/chromedriver_linux"
        elif "win32" in sys.platform:
            executable_path ="./bin/chromedriver_win"
        else:
            raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = webdriver.Chrome(executable_path=executable_path, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    elif args.driver_type == "opera":
        if args.headless:
            options.add_argument("--headless")
        if sys.platform == "win32":
            executable_path =   "./bin/operadriver_win64"
        else:
            raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = webdriver.Opera(executable_path=executable_path)

    elif args.driver_type == "uc":

        options = uc.ChromeOptions()
        ua = UserAgent()
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
        print(userAgent)
        ##'geolocation': 2, 'durable_storage': 2, 
        # prefs = {'profile.default_content_setting_values': { 'images': 2,
        #                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
        #                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
         #                   'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
         #                   'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
         #                   'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
         #                   'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'dom.webdriver.enabled': 2, 'useAutomationExtension':2}}
        #options.add_experimental_option('prefs', prefs)
        #options.add_argument("--start-maximized")
        #options.add_argument("--disable-infobars")
        #options.add_argument("--disable-extensions")
        #options.add_argument("--incognito")
        #options.add_argument(f'user-agent={userAgent}')
        #options.add_argument("--lang=pt-br")
        #options.add_argument("--disable-blink-features=AutomationControlled") #

        if args.headless:
            options.add_argument("--headless")
        #if sys.platform == "darwin":
        #    executable_path = "./bin/chromedriver_mac"
        #elif "linux" in sys.platform:
        #    executable_path = "./bin/chromedriver_linux"
       # elif "win32" in sys.platform:
        #    executable_path ="./bin/chromedriver_win"
        #else:
        #    raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = uc.Chrome(options=options)



run(driver=driver, username=args.username, password=args.password, url=args.url, shoe_size=args.shoe_size, deliver_type=args.deliver_type,
        login_time=args.login_time, release_time=args.release_time, page_load_timeout=args.page_load_timeout,
        screenshot_path=args.screenshot_path, html_path=args.html_path, select_payment=args.select_payment,
        purchase=args.purchase, num_retries=args.num_retries)

