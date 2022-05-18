from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os
import urllib.request
import pyperclip
from selenium.webdriver.common.keys import Keys

EXTENSION_PATH = os.getcwd() + '\metamaskExtension.crx'

EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'


def downloadMetamaskExtension():
    print('设置小狐狸')
    print('Setting up metamask extension please wait...')

    url = 'https://xord-testing.s3.amazonaws.com/selenium/10.0.2_0.crx'
    urllib.request.urlretrieve(url, os.getcwd() + '/metamaskExtension.crx')


def launchSeleniumWebdriver(driverPath):
    print('path', EXTENSION_PATH)
    chrome_options = Options()
    chrome_options.add_extension(EXTENSION_PATH)
    global driver
    driver = webdriver.Chrome(options=chrome_options, executable_path=driverPath)
    time.sleep(5)
    print('小狐狸已加载')
    print("Extension has been loaded")
    return driver


def metamaskSetup(recoveryPhrase, password):

    driver.switch_to.window(driver.window_handles[0])

    driver.find_element_by_xpath('//button[text()="开始使用"]').click()
    driver.find_element_by_xpath('//button[text()="导入钱包"]').click()
    driver.find_element_by_xpath('//button[text()="不，谢谢"]').click()

    time.sleep(1)
    #修改适配新版本小狐狸
    pyperclip.copy(recoveryPhrase)
    
    input = driver.find_elements_by_xpath('//*[@id="import-srp__srp-word-0"]')
    input[0].send_keys(Keys.CONTROL,'v')
    input1 = driver.find_elements_by_xpath('//*[@id="password"]')
    input1[0].send_keys(password)
    input2 = driver.find_elements_by_xpath('//*[@id="confirm-password"]')
    input2[0].send_keys(password)
    
    driver.find_element_by_xpath('//*[@id="create-new-vault__terms-checkbox"]').click()
    driver.find_element_by_xpath('//button[text()="导入"]').click()

    time.sleep(5)

    driver.find_element_by_xpath('//button[text()="全部完成"]').click()
    time.sleep(2)

    # closing the message popup after all done metamask screen
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/div[1]/div/button').click()
    time.sleep(2)
    print("钱包导入完成")
    print("Wallet has been imported successfully")
    time.sleep(10)


def changeMetamaskNetwork(networkName):
    # opening network
    print("改变网络")
    print("Changing network")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    time.sleep(2)
    print("opening network dropdown")
    elem = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div')
    time.sleep(2)
    all_li = elem.find_elements_by_tag_name("li")
    time.sleep(2)
    for li in all_li:
        text = li.text
        if (text == networkName):
            li.click()
            print(text, "is selected")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
            return
    time.sleep(2)
    print("Please provide a valid network name")

    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def connectToWebsite():
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    time.sleep(3)
    print('连接网站成功')
    print('Site connected to metamask')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

#同意交易授权
def confirmApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(15)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[6]/footer/button[2]').click()
    #授权网络//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]
    #授权交易//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[2]
    time.sleep(12)
    print("Approval transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
#############################
#同意添加网络授权
def confirmApprovalChangeNetowrkFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(15)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/button[2]').click()
    #授权网络//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]
    #授权交易//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[2]
    time.sleep(12)
    print("Approval transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
#############################
#授权后切换网络
def confirmSwitchNetwork():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/button[2]').click()
    time.sleep(12)
    print("Approval transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
#############################

def rejectApprovalFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(10)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[4]/footer/button[1]').click()
    time.sleep(8)
    print("Approval transaction rejected")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
    print("Reject approval from metamask")

#同意交易
def confirmTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(10)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(15)

    # # confirm transaction from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[5]/div[3]/footer/button[2]').click()
    time.sleep(13)
    print("Transaction confirmed")

    # switch to dafi
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(3)


def rejectTransactionFromMetamask():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)
    # confirm approval from metamask
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[1]').click()
    time.sleep(2)
    print("Transaction rejected")

    # switch to web window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

def addToken(tokenAddress):
    # opening network
    print("Adding Token")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('chrome-extension://{}/home.html'.format(EXTENSION_ID))
    print("closing popup")
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()

    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    # time.sleep(2)

    print("clicking add token button")
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/div/div[3]/button').click()
    time.sleep(2)
    # adding address
    driver.find_element_by_id("custom-address").send_keys(tokenAddress)
    time.sleep(10)
    # clicking add
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/footer/button[2]').click()
    time.sleep(2)
    # add tokens
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[3]/footer/button[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
#同意签名
def signConfirm():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]').click()
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign confirmed')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


def signReject():
    print("sign")
    time.sleep(3)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get('chrome-extension://{}/popup.html'.format(EXTENSION_ID))
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[1]').click()
    time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(3)
    print('Sign rejected')
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)
