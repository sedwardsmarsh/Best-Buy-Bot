from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import info
import links
import os
from datetime import datetime

def bot():
    # get PID
    PID = os.getpid()

    # initialize webbrowser "driver" object
    opts = ChromeOptions()
    driver = webdriver.Chrome(options=opts)

    # default wait mechanism for all elements
    wait = WebDriverWait(driver, 10, poll_frequency=1)

    # variable to store if script has completed or not
    # variable is updated based on whether a file has been created in the directory of the script
    # the file will be named DONE
    isComplete = False
    if os.path.exists('./DONE'):
        isComplete = True

    # keep track of when script starts
    time_start = datetime.now()

    # load first best buy link
    link_arr = links.link_arr
    link_idx = 0
    driver.get(link_arr[0])

    while not isComplete:
        # find add to cart button
        try:
            atcBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button')))
        except:
            # load next link in array
            link_idx = (link_idx + 1) % len(link_arr)
            driver.get(link_arr[link_idx])
            print(f'switching to link: {link_arr[link_idx]}')
            continue

        try:
            # add to cart
            atcBtn.click()
            print(f'PID: {PID} added item to cart')

            # go to cart and begin checkout as guest
            driver.get('https://www.bestbuy.com/cart')
            print(f'PID: {PID} navigated to cart')

            # click checkout button
            checkoutBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-lg.btn-block.btn-primary')))
            checkoutBtn.click()
            print(f'PID: {PID} navigating to checkout')

            # fill in email
            emailField = wait.until(EC.element_to_be_clickable((By.ID, 'fld-e')))
            emailField.send_keys(info.email)
            print(f'PID: {PID} entered email')

            # fill in password and press enter
            pwdField = wait.until(EC.element_to_be_clickable((By.ID, 'fld-p1')))
            pwdField.send_keys(info.password)
            pwdField.send_keys(Keys.ENTER)
            print(f'PID: {PID} entered password')

            # switch to shipping if its not selected
            shippingLink = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.ispu-card__switch')))
            if shippingLink.text == 'Switch to Shipping':
                shippingLink.click()
                print(f'PID: {PID} switched from pickup to shipping')
            else:
                print(f'PID: {PID} shipping already selected')

            # fill in card cvv
            cvvField = wait.until(EC.element_to_be_clickable((By.ID, 'cvv')))
            cvvField.send_keys(info.cvv)
            print(f'PID: {PID} entered cvv')

            # place order
            # WARNING: uncommenting the code below will allow the bot to make purchases autonomously!!!
            # placeOrderBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button__fast-track')))
            # placeOrderBtn.click()

            # make the file: DONE in the local directory, which tells the script to stop running
            open('./DONE', 'w')
            isComplete = True
        except:
            # make sure this link is the same as the link passed to driver.get() before looping
            link_idx = (link_idx + 1) % len(link_arr)
            driver.get(link_arr[link_idx])
            print(f'Error - restarting bot and switching link to: {link_arr[link_idx]}\n')
            continue

    # get finish time of script
    time_end = datetime.now()
    print(f'PID: {PID} Order successfully placed')
    print(f'total time: {time_end - time_start}')
    driver.close()

cwd = os.getcwd()
process_dir = f'{cwd}/BestBuyBot - {datetime.now()}'
os.mkdir(process_dir)
os.chdir(process_dir)
bot()