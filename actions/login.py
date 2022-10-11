

def login(driver, username, password, TimeoutException):
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