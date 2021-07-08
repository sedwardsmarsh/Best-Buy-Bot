from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
# import chromedriver_autoinstaller

import info
import links

# initialize webbrowser "driver" object
driver = webdriver.Chrome(ChromeDriverManager().install())

# load best buy store page for xbox series x
driver.get(links.PNY_32GB_USB_STICK)

# time interval to wait for each

isComplete = False

while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.add-to-cart-button'))
        )
    except:
        driver.refresh()
        continue

    print('Add to cart button found')

    try:
        # add to cart
        atcBtn.click()
        print('debug: added to cart')

        # go to cart and begin checkout as guest
        driver.get('https://www.bestbuy.com/cart')
        print('debug: navigated to cart')

        # click checkout button
        checkoutBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-lg.btn-block.btn-primary'))
        )
        checkoutBtn.click()
        print('Successfully added to cart - beginning check out')

        # fill in email
        emailField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'fld-e')))
        emailField.send_keys(info.email)
        print('debug: entered email')

        # fill in password and press enter
        pwdField = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'fld-p1')))
        pwdField.send_keys(info.password)
        pwdField.send_keys(Keys.ENTER)
        print('debug: entered password')

        # switch to shipping
        shippingLink = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ispu-card__switch')))
        shippingLink.click()

        # fill in card cvv
        cvvField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'cvv'))
        )
        cvvField.send_keys(info.cvv)
        print('debug: entered cvv')

        # place order
        # placeOrderBtn = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '.button__fast-track'))
        # )
        # placeOrderBtn.click()

        isComplete = True
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        driver.get(links.PNY_32GB_USB_STICK)
        print('Error - restarting bot')
        continue

print('Order successfully placed')



