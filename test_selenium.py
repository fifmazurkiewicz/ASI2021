import time

from selenium import webdriver

username, password = "testuser", "test1234"
driver = webdriver.Chrome("chromedriver.exe")
own_site_url = "http://127.0.0.1:5000/"

# own_site_url = "https://ZadanieASI.filipmazurkiewi.repl.co"

def register_user():
    nasz_url = own_site_url + '/signup'
    driver.get(nasz_url)
    user_input = driver.find_element_by_name("username")
    passwd = driver.find_element_by_name("password")

    user_input.send_keys(username)
    passwd.send_keys(password)

    submitbutton = driver.find_element_by_xpath("//input[@type='submit']")
    submitbutton.submit()
    return username, password


def login_user(username, password):
    nasz_url = own_site_url
    driver.get(nasz_url)
    user_input = driver.find_element_by_name("username")
    passwd = driver.find_element_by_name("password")
    user_input.send_keys(username)
    passwd.send_keys(password)
    submitbutton = driver.find_element_by_xpath("//input[@type='submit']")
    submitbutton.submit()


def test_cutsie():
    gif = driver.find_element_by_id('cutsie.gif')
    size = gif.size
    width = float(size["width"])
    assert width >= 100
    height = float(size["height"])
    assert height >= 100


def test_pogoda_dla_wyszukanego_miasta():
    cities = ["Poznań", "Warszawa", "Zaw", "Katowice"]
    nasz_url = own_site_url + '/weather'
    driver.get(nasz_url)
    city_input = driver.find_element_by_name("search")
    city_input.send_keys(username)
    nasz_url = own_site_url + '/weather'
    driver.get(nasz_url)
    for i in cities:
        time.sleep(0.5)
        city_input = driver.find_element_by_name("search")
        city_input.send_keys(i)
        driver.implicitly_wait(50)
        submitbutton = driver.find_element_by_xpath("//input[@type='submit']")
        submitbutton.submit()


def test_dodanie_oceny():
    nasz_url = own_site_url + '/grades'
    driver.get(nasz_url)
    submitbutton = driver.find_element_by_xpath("//input[@type='submit']")
    submitbutton.submit()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def test_przekierowania_na_otomoto():
    nasz_url = own_site_url + '/predict'
    driver.get(nasz_url)
    link = driver.find_element_by_link_text('Otomoto example')
    link.click()
    window_name = driver.window_handles[1]
    driver.switch_to.window(window_name=window_name)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    time.sleep(2)
    oferta_cena = driver.find_element_by_xpath('//*[@class="offer-price__number ds-price-number"]')
    driver.execute_script("window.scrollTo(0, 500)")
    highlight(oferta_cena, 2.5, "blue", 2.5)
    driver.close()
    window_name = driver.window_handles[0]
    driver.switch_to.window(window_name=window_name)
    nasz_url = own_site_url + '/predict'
    driver.get(nasz_url)
    time.sleep(2)


def test_wyceny_samochodu():
    nasz_url = own_site_url + '/predict'
    driver.get(nasz_url)
    rok = 2005
    rok_input = driver.find_element_by_name("Production_year")
    rok_input.send_keys(rok)
    przebieg = 350000
    przebieg_input = driver.find_element_by_name("Mileage_km")
    przebieg_input.send_keys(przebieg)
    moc = 155
    moc_input = driver.find_element_by_name("Power_HP")
    moc_input.send_keys(moc)

    pojemnosc = 1997
    pojemnosc_input = driver.find_element_by_name("Displacement_cm3")
    pojemnosc_input.send_keys(pojemnosc)
    drzwi = 3
    drzwi_input = driver.find_element_by_name("Doors_number")
    drzwi_input.send_keys(drzwi)
    stan = "Used"
    stan_input = driver.find_element_by_name("Condition")
    stan_input.send_keys(stan)

    marka = "Peugeot"
    marka_input = driver.find_element_by_name("Vehicle_brand")
    marka_input.send_keys(marka)
    model = 307
    model_input = driver.find_element_by_name("Vehicle_model")
    model_input.send_keys(model)
    drive = "Front wheels"
    drive_input = driver.find_element_by_name("Drive")
    drive_input.send_keys(drive)
    transmission = "manual"
    transmission_input = driver.find_element_by_name("Transmission")
    transmission_input.send_keys(transmission)
    type = "convertible"
    type_input = driver.find_element_by_name("Type")
    type_input.send_keys(type)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submitbutton = driver.find_element_by_xpath("//input[@type='submit']")
    time.sleep(1)
    submitbutton.submit()
    driver.execute_script("window.scrollTo(0,0)")
    open_window_elem = driver.find_element_by_id("result")
    highlight(open_window_elem, 3, "blue", 5)


def highlight(element, effect_time, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)

    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color))
    time.sleep(effect_time)
    apply_style(original_style)


def test_wylogowanie():
    nasz_url = own_site_url + '/wyloguj'
    driver.get(nasz_url)


def test_oursite():
    username, password = register_user()
    nasz_url = own_site_url
    driver.get(nasz_url)
    login_user(username, password)
    test_cutsie()
    test_pogoda_dla_wyszukanego_miasta()
    test_dodanie_oceny()
    test_wyceny_samochodu()
    test_przekierowania_na_otomoto()
    test_wylogowanie()


test_oursite()
