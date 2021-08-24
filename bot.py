from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from webdriver_manager.chrome import ChromeDriverManager
import info
import links
import os
import time
from datetime import datetime

# initialize webbrowser "driver" object
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Safari()

# load best buy store page for items
driver.get(links.PNY_32GB_USB_STICK)

# default wait mechanism for all elements
wait = WebDriverWait(driver, 10, poll_frequency=1)

sleep_delay = 0

# variable to store if script has completed or not
# variable is updated based on whether a file has been created in the directory of the script
# the file will be named DONE
isComplete = False
# if os.path.exists('./DONE'):
#     isComplete = True

# keep track of when script starts
time_start = datetime.now()

while not isComplete:
    # find add to cart button
    try:
        atcBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button')))
    except:
        driver.refresh()
        continue

    print('Added item to cart')

    try:
        # add to cart
        atcBtn.click()
        print('added to cart')

        # go to cart and begin checkout as guest
        driver.get('https://www.bestbuy.com/cart')
        print('navigated to cart')

        # time.sleep(sleep_delay)

        # click checkout button
        checkoutBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'btn.btn-lg.btn-block.btn-primary')))
        checkoutBtn.click()
        print('added item to cart - beginning check out')

        # fill in email
        emailField = wait.until(EC.element_to_be_clickable((By.ID, 'fld-e')))
        emailField.send_keys(info.email)
        print('entered email')

        # time.sleep(sleep_delay)

        # fill in password and press enter
        pwdField = wait.until(EC.element_to_be_clickable((By.ID, 'fld-p1')))
        pwdField.send_keys(info.password)
        pwdField.send_keys(Keys.ENTER)
        print('entered password')

        # time.sleep(sleep_delay)

        # switch to shipping if its not selected
        shippingLink = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ispu-card__switch')))
        if shippingLink.text == 'Switch to Shipping':
            shippingLink.click()
            print('switched from pickup to shipping')
        else:
            print('shipping already selected')

        # time.sleep(sleep_delay)

        # fill in card cvv
        cvvField = wait.until(EC.element_to_be_clickable((By.ID, 'cvv')))
        cvvField.send_keys(info.cvv)
        print('entered cvv')

        # place order
        # WARNING: uncommenting the code below will allow the bot to make purchases autonomously!!!
        # placeOrderBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button__fast-track')))
        # placeOrderBtn.click()

        # make the file: DONE in the local directory, which tells the script to stop running
        open('./DONE', 'w')
        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(links.PNY_32GB_USB_STICK)
        print('Error - restarting bot\n')
        continue

# get finish time of script
time_end = datetime.now()
print('Order successfully placed')
print(f'total time: {time_end - time_start}')
driver.close()