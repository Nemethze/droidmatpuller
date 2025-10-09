import os
from time import sleep
import uiautomator2 as u
import random

Gport = 0
Gkeyword = ""
Gtime = 1
Gblacklist = []
GmaxAd = 1
Gsec = 0
Gstop = False
GcookieList = []

def readinFile():
    os.system("rm config.txt")
    os.system("wget https://raw.githubusercontent.com/Nemethze/droidmatpuller/refs/heads/main/config.txt")
    with open("config.txt", "r") as file:
        lines = file.readlines()
    with open("port.txt","r") as file2:
        lines2 = file2.readlines()
        
    global Gtime, Gkeyword, Gblacklist, GmaxAd, Gport, Gsec, Gstop, GcookieList
    Gtime = int(lines[1].strip())
    Gkeyword = lines[3].strip().split(", ")
    Gblacklist = lines[5].strip().split(", ")
    GmaxAd = int(lines[7].strip())
    Gport = int(lines2[1].strip())
    Gsec = int(lines[9].strip())
    Gstop = bool(lines[13].strip())
    GcookieList = lines[11].strip().split(", ")


def airplaneMode(time):
    os.system("sudo settings put global airplane_mode_on 1")
    sleep(time)
    os.system("sudo settings put global airplane_mode_on 0")


def search(keyword):
    d.app_start("com.android.chrome")
    sleep(random.uniform(2,4))

    d(resourceId="com.android.chrome:id/menu_button").click()
    sleep(random.uniform(1,2))
    d(text="New Incognito tab").click()
    sleep(random.uniform(2,4))

    address_bar = d(className="android.widget.EditText")
    address_bar.click()
    d.send_keys(keyword)
    d.press("enter")
    sleep(random.uniform(3,5))

    for _ in range(2):
        d.swipe(500, 1700, 500, 800)  
        sleep(random.uniform(1,2))

    d.click(540, 1925)
    print("Cookie popup elutasítva (koordináta alapján).")
    sleep(random.uniform(1,2))

     
def openAd(maxAds):
    sleep(2)

    ads_opened = 0
    last_y = 0

    # Szponzorált felirat keresése egyszer
    spon_elems = d(textContains="Szponzorált")
    if str(spon_elems) == len(spon_elems) > 0:
        ad = spon_elems[0]
        info = ad.info
        bounds = info.get("bounds")
        if not bounds:
            print("Nincs érvényes bounds a szponzorált elemhez")
            return
        spon_y = (bounds["top"] + bounds["bottom"]) // 2
        print(f"Első 'Szponzorált' elem megtalálva, y={spon_y}")
    if not spon_elems:
        print("Nincs 'Szponzorált' találat, alap lokáció")
        spon_y = 750 
    
    

    # Első szponzorált elem pozíciója


    while ads_opened < maxAds:
        try:
            # Blacklist ellenőrzés az egész kijelzőn
            blacklist_hit = False
            for b in Gblacklist:
                if not b:
                    continue
                all_text_elems = d.xpath(f'//*[contains(@text, "{b}")]').all()
                for elem in all_text_elems:
                    t_bounds = elem.info.get("bounds", {})
                    if not t_bounds:
                        continue
                    t_x = (t_bounds["left"] + t_bounds["right"]) // 2
                    if 0 <= t_x <= 450:  # 220 ±100
                        blacklist_hit = True
                        print(f" → Átugrom, mert blacklist találat: '{b}' x={t_x}")
                        d.swipe(510, 1700, 155, 1700)  # görget tovább
                        break
                if blacklist_hit:
                    break

            if blacklist_hit:
                continue

            # Ha nem blacklistes → long click 500px-el lejjebb, X=150
            click_y = 1300
            try:
                d.long_click(150, click_y, 2)
                sleep(random.uniform(2,3))

                if d(text="Open in new tab").exists(timeout=2):
                    d(text="Open in new tab").click()
                    ads_opened += 1
                    print(f"{ads_opened}. hirdetés megnyitva")
                    sleep(random.uniform(2,3))
                    d.click(900, 150)  # új fülre váltás
                    sleep(random.uniform(2,3))
                    d.click(830, 680)  # első katt az oldalon
                    sleep(random.uniform(2,3))
                    siteVisit()
                    sleep(random.uniform(2,3))
                    d.swipe(510, 1700, 155, 1700)  # görgetés
                else:
                    print("Nem találtam 'Open in new tab' opciót")

            except Exception as e:
                print("Long click hiba:", e)
                continue

        except Exception as e:
            print("Hirdetés megnyitási hiba:", e)
            break


# Globális flag
clicked_homelux = False

def siteVisit():
    global clicked_homelux
    sleep(random.uniform(3,4))

    # Ha a weboldal tartalmazza a 'homelux.hu' részt és még nem kattintottunk → egyszeri kattintás
    try:
        current_url = d.info.get("currentPackageName", "")
        try:
            # egyes uiautomator2 verziókban így kérhető az URL
            current_url = d.xpath('//android.widget.EditText').get().get_text()
        except:
            pass

        if d(text="Adatkezelési beállítások").exists(timeout=2):
            print("homelux.hu észlelve → egyszeri kattintás (780,800)")
            try:
                d.click(780, 800)
                clicked_homelux = True
                sleep(random.uniform(1.5,3))
            except Exception as e:
                print("Hiba a homelux.hu kattintásnál:", e)
    except Exception as e:
        print("Nem sikerült az URL ellenőrzése:", e)

    # Cookie elfogadás keresése
    for cookie_text in GcookieList:
        try:
            if d(text=cookie_text).exists(timeout=2):
                print(f"→ '{cookie_text}' gomb megtalálva, kattintás...")
                try:
                    d(text=cookie_text).click()
                    sleep(random.uniform(1.5,3))
                    break  # stop after first successful click
                except Exception as e:
                    print(f"Nem sikerült kattintani a(z) '{cookie_text}' gombra:", e)
        except Exception as e:
            print(f"Hiba a(z) '{cookie_text}' keresésénél:", e)

    # Görgetés vagy várakozás
    if Gsec > 0:
        for i in range(Gsec):
            d.swipe(540, 2000, 540, 370)
            sleep(random.uniform(0.5,2))
    else:
        sleep(random.uniform(2,5))

    d.press("back")



def close():
    d.press("home")
    d.shell("am force-stop com.android.chrome")



while Gstop == False:
    readinFile()
    d = u.connect(f"127.0.0.1:{Gport}")
    for k in Gkeyword:
        airplaneMode(Gtime)
        os.system("curl ifconfig.me")
        search(k)
        openAd(GmaxAd)
        close()
