from time import sleep, time
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as Chromeoptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
        TimeoutException, UnexpectedAlertPresentException, NoSuchElementException, WebDriverException,
        ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from tkinter import * 
from tkinter import messagebox
import asyncio
import csv
#-----------------------------statics----------------------------
IMPORTANT_WAIT= 5
IMPORTANT_TINY_WAIT= 3
DONT_CARE_WAIT= 1000
TINY_WAIT=0.5
RETRY_XPATH = "//*[@id=\"app\"]/div[1]/div[1]/div/button"

tokens = []
file = open('tokens.csv')
tokenreader = csv.reader(file)
for row in tokenreader:
    tokens.append(row[0])
#----------------------------tkinter init----------------------------
SEND_MESSAGE = False
SAVE_POST = False

root = Tk()
root.title('divar bot')
root.geometry('250x350')
photo = PhotoImage(file = "divar-logo.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=False)
bg_color, framecolor = '#00007a', '#ffbb00'
root.config(bg=bg_color)
#-----------------------------Frames-------------------------------
Top_First = Frame(root, width=400, height=50, bg=framecolor) # check boxes
Top_First.pack(side='top')
Top_Second = Frame(root, width=400, height=20, bg=bg_color) # result of check boxes
Top_Second.pack(side='top')
Top_First_Temp = Frame(root, width=400, height=20, bg=bg_color) # blank space
Top_First_Temp.pack(side='top')
Top_Third = Frame(root, width=180, height=20, bg=framecolor) # label for 
Top_Third.pack(side='top')
Top_Fourth = Frame(root, width=80, height=90, bg=framecolor) # input search text
Top_Fourth.pack(side='top')
Top_Second_Temp = Frame(root, width=400, height=40, bg=bg_color) # blank space
Top_Second_Temp.pack(side='top')
Top_Fifth = Frame(root, width=400, height=50, bg=framecolor)
Top_Fifth.pack(side='top')
Top_Third_Temp = Frame(root, width=400, height=57, bg=bg_color) # blank space
Top_Third_Temp.pack(side='top')
Top_Seventh = Frame(root, width=400, height=50, bg=framecolor)
Top_Seventh.pack(side='top')

#---------------------------functions----------------------------
def checks_config():
    global SAVE_POST, SEND_MESSAGE
    if savevar.get() == 1 and msgvar.get() == 1:
        SAVE_POST, SEND_MESSAGE = True, True
        l.config(text='هر دو گزینه نشان و پیام فعال است')
    elif savevar.get() == 0 and msgvar.get() == 1:
        SAVE_POST, SEND_MESSAGE = False, True
        l.config(text='گزینه پیام دادن فعال است')
    elif savevar.get() == 1 and msgvar.get() == 0:
        SAVE_POST, SEND_MESSAGE = True, False
        l.config(text='گزینه نشان کردن فعال است')
    else:
        SEND_MESSAGE, SAVE_POST = False, False
        l.config(text='(هیچ گزینه ای فعال نیست) فقط سین میزند')


def quit_window():
    root.destroy()


def about():
    messagebox.showinfo('about', 'this bot can view, save post and send message to announcer \nprogrammed by @soroush_fathi')


def retry(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    except NoSuchElementException:  
        pass  


def start_program(event = None):
    searchinputs = [searchinput1, searchinput2, searchinput3]
    searchtxts = [x.get(1.0, "end-1c") for x in searchinputs]
    if not any([x != '' for x in searchtxts]):
        return messagebox.showinfo('خطا', 'فیلد های سرچ نباید خالی باشد')
    searchtxts = list(filter(None, searchtxts))
    root.destroy()
    options = Chromeoptions()
    options.page_load_strategy = 'eager'
    # options.add_experimental_option('debuggerAddress', 'localhost:9222')
    options.add_argument('--disable-notifications')
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2 }) 
    # driver = Chrome(options=options)
    driver = Chrome(executable_path='chromedriver.exe', options=options)
    for searchtxt in searchtxts:
        for token in tokens:
            # driver.switch_to.window(driver.window_handles[x])
            initurl =  "https://divar.ir"
            driver.get(initurl)
            driver.add_cookie({'name': 'token', 'value': f'{token}'})
            driver.maximize_window()
            mshdxpath = "//*[@id=\"app\"]/div[1]/div[3]/div[1]/div/div[2]/div[2]/a[2]"
            WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, mshdxpath))).click()  # click on Mashhad

            xpath = "//*[@id=\"app\"]/header/nav/div/div[2]/div/div[1]/form/input"  # click on search input then press enter
            WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(f'{searchtxt}')    
            WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(Keys.ENTER)    

            productsclass = "kt-post-card__features"
            items = None
            try:    
                items = WebDriverWait(driver, timeout=IMPORTANT_WAIT).until(EC.presence_of_all_elements_located((By.CLASS_NAME, productsclass)))
            except TimeoutException:
                print('آیتمی بااین موضوع یافت نشد')

            if items:
                n = len(items)
                for i in range(n):                    
                    try:
                        items = WebDriverWait(driver, timeout=DONT_CARE_WAIT, poll_frequency=3, ignored_exceptions=None).until(EC.presence_of_all_elements_located((By.CLASS_NAME, productsclass)))
                        n = len(items)
                        items[i].click()
                    except (IndexError, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException):
                        print('آیتم برای کلیک کردن آماده نبود')
                        break
                    
                    retry(driver, RETRY_XPATH)
                    
                    if SAVE_POST and (not i % 4):
                        xpath = "//*[@id=\"app\"]/div[1]/div/div[1]/div[2]/span[1]/button"
                        WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                    if SEND_MESSAGE and (not i % 5):
                        xpath = "//*[@id=\"app\"]/div[1]/div/div[1]/div[2]/button[2]"  # start chat button
                        if bts:=WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))):
                            bts.click()
                            if i==0:  # first time fro accepting rules
                                xpath = "/html/body/div[2]/div/div/div/footer/button"
                                if nbts:=WebDriverWait(driver, timeout=IMPORTANT_TINY_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))):
                                    nbts.click()
                        if i == 0:
                            driver.add_cookie({'name': 'token', 'value': f'{token}'})
                            driver.refresh()
                        
                        xpath = "//*[@id=\"root\"]/main/div/div/div[3]/div[2]/div/input"
                        msgtxt = "سلام، هنوز موجوده؟"
                        WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).send_keys(f'{msgtxt}')
                        xpath = "//*[@id=\"root\"]/main/div/div/div[3]/div[2]/div/button"
                        # WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                        driver.back()
                        driver.back()
                    driver.back()
                    per_row = 2
                    driver.execute_script(f"window.scrollTo(0, 150*{i//per_row})")
            # todo: check changing token
            driver.delete_all_cookies()
    driver.quit()


root.bind('<Return>', start_program)

def close_win(e):
    root.destroy()

root.bind('<Escape>', lambda e: close_win(e))
#---------------------------Buttons & Checkbuttons---------------------------
savevar = IntVar()
savebtn = Checkbutton(Top_First, text='نشان کردن',variable=savevar, onvalue=1, offvalue=0, command=checks_config)
savebtn.pack(side=LEFT, padx=3, pady=3)
msgvar = IntVar()
msgbtn = Checkbutton(Top_First, text='پیام دادن', variable=msgvar, onvalue=1, offvalue=0, command=checks_config)
msgbtn.pack(side=RIGHT, padx=3, pady=3)

l = Label(Top_Second, bg='white', width=50, text='(هیچ گزینه ای فعال نیست) فقط سین میزند')
l.pack(side=LEFT, padx=5, pady=5)

lbl = Label(Top_Third, text=':عنوانی که میخواهید ربات سرچ کند را وارد کنید', bg=framecolor)
lbl.pack()

searchinput1 = Text(Top_Fourth, width=20, height=1)
searchinput1.pack(padx=5, pady=5)
searchtxt1 = searchinput1.get(1.0, "end-1c")

searchinput2 = Text(Top_Fourth, width=20, height=1)
searchinput2.pack(padx=5, pady=5)
searchtxt2 = searchinput2.get(1.0, "end-1c")

searchinput3 = Text(Top_Fourth, width=20, height=1)
searchinput3.pack(padx=5, pady=5)
searchtxt3 = searchinput3.get(1.0, "end-1c")

startbtn = Button(Top_Fifth, text='شروع', width=15, command=start_program)
startbtn.pack(side=TOP, padx=1, pady=1)
startbtn = Button(Top_Seventh, text='خروج', width=8, command=quit_window)
startbtn.pack(side=RIGHT, padx=1, pady=1)
startbtn = Button(Top_Seventh, text='درباره', width=8, command=about)
startbtn.pack(side=LEFT, padx=1, pady=1)
#----------------------------main tkinter---------------------------
root.mainloop()
