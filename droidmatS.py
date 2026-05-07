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
Gstop = "False"
GcookieList = []
location = ""
config_num = ""
phone_type = ""


def readinFile():
    global location, config_num, phone_type
    with open("config_local.txt","r") as file3:
        lines3 = file3.readlines()
    location = lines3[1].strip()
    config_num = lines3[3].strip()
    phone_type = lines3[5].strip()
    
    os.system(f"rm config_{config_num}.txt")
    os.system(f"wget https://raw.githubusercontent.com/Nemethze/droidmatpuller/refs/heads/main/config_{config_num}.txt")
    try:
        with open(f"config_{config_num}.txt", "r") as file:
            lines = file.readlines()
    except:
        os.system(f"rm config.txt")
        os.system(f"wget https://raw.githubusercontent.com/Nemethze/droidmatpuller/refs/heads/main/config.txt")
        with open("config.txt", "r") as file:
            lines = file.readlines()
    with open("port.txt","r") as file2:
        lines2 = file2.readlines()

        
    global Gtime, Gkeyword, Gblacklist, GmaxAd, Gport, Gsec, Gstop, GcookieList, Gshopstop
    Gtime = int(lines[1].strip())
    Gkeyword = lines[3].strip().split(", ")
    Gblacklist = lines[5].strip().split(", ")
    GmaxAd = int(lines[7].strip())
    Gport = int(lines2[1].strip())
    Gsec = int(lines[9].strip())
    Gstop = lines[15].strip()
    GcookieList = lines[11].strip().split(", ")
    Gshopstop = int(lines[13].strip())

def airplaneMode(time):
    os.system("sudo settings put global airplane_mode_on 1")
    sleep(time)
    os.system("sudo settings put global airplane_mode_on 0")


def search(keyword):
    global phone_type
    d.app_start("com.android.chrome")
    if phone_type == "4g":
        sleep(random.uniform(2,4))
        d.click(50, 300)
        sleep(random.uniform(0.5,1))
    
        d.click(1020, 185)
        sleep(random.uniform(1,2))
        d.click(700, 420)
        sleep(random.uniform(2,4))
    
        d.click(580, 180)
        d.send_keys(keyword)
        d.press("enter")
        sleep(random.uniform(3,5))
    
        for _ in range(2):
            d.swipe(500, 1700, 500, 800)  
            sleep(random.uniform(1,2))
    
        d.click(540, 1925)
        print("Cookie popup elutasítva (koordináta alapján).")
        sleep(random.uniform(1,2))
    if phone_type == "5g":
        d.app_start("com.android.chrome")
        sleep(random.uniform(2,4))
        d.click(200, 200)
        sleep(random.uniform(0.5,1))
    
        d.click(700, 150)
        sleep(random.uniform(1,2))
        d.click(440, 320)
        sleep(random.uniform(2,4))
    
        d.click(360, 140)
        d.send_keys(keyword)
        d.press("enter")
        sleep(random.uniform(3,5))
    
        for _ in range(2):
            d.swipe(360, 1100, 360, 360)  
            sleep(random.uniform(1,2))
    
        d.click(360, 1280)
        print("Cookie popup elutasítva (koordináta alapján).")
        sleep(random.uniform(1,2))


def clickInstr(maxAdsInner):
    global phone_type, location
    ads_opened = 0
    skipped_ads = 0
    skipped_sites = 0
    while ads_opened < maxAdsInner:
        try:
            blacklist_hit = False
            if phone_type == "4g":
                d.long_click(150, 1650, 2)
            if phone_type == "5g":
                d.long_click(70, 1240, 2)
            sleep(random.uniform(2,3))
            if phone_type == "4g":
                d.click(540, 780)
            if phone_type == "5g":
                d.click(360, 500)
            for b in Gblacklist:
                if d(textContains=b).exists(timeout=0.5):
                    blacklist_hit = True
                    print(f" → Átugrom, mert blacklist találat: '{b}'")
                    blacklist_hit = True
                    if phone_type == "4g":
                        d.click(1010, 2300)
                    if phone_type == "5g":
                        d.click(650, 1470)
                    sleep(random.uniform(0.5,1))
                    if phone_type == "4g":
                        d.swipe(510, 1700, 155, 1700)
                    if phone_type == "5g":
                        d.swipe(360, 1280, 50, 1280)
                    skipped_ads += 1
                    print(f"Átugrott hirdetések száma {skipped_ads}")
                    break
            if skipped_ads > 5:
                print("Sok egymás utánni hirdetés")
                break
            if location == "m":
                if d(textContains="Továbbiak:").exists(timeout=2) or d(textContains="Felkeresés:").exists(timeout=2):
                    break
            if phone_type == "r":
                if d(textContains="Accesează").exists(timeout=2) or d(textContains="Mai multe de la").exists(timeout=2):
                    break
            if blacklist_hit == False:
                try:
                    if d(text="Open in new tab").exists(timeout=2):
                        skipped_ads = 0
                        d(text="Open in new tab").click()
                        ads_opened += 1
                        print(f"{ads_opened}. hirdetés megnyitva")
                        sleep(random.uniform(2,3))
                        if phone_type == "4g":
                            d.click(900, 150)  # új fülre váltás
                        if phone_type == "5g":
                            d.click(590, 100)  # új fülre váltás
                        sleep(random.uniform(2,3))
                        if phone_type == "4g":
                            d.click(830, 680)  # első katt az oldalon
                        if phone_type == "5g":
                            d.click(500, 500)  # első katt az oldalon
                        sleep(random.uniform(2,3))
                        siteVisit()
                        sleep(random.uniform(2,3))
                        if phone_type == "4g":
                            d.swipe(510, 1700, 163, 1700)  # görgetés
                        if phone_type == "5g":
                            d.swipe(360, 1280, 50, 1280)  # görgetés
                        sleep(random.uniform(3,4))
                    else:
                        print("Nem találtam 'Open in new tab' opciót")
                        break
            
                except Exception as e:
                    print("Long click hiba:", e)
                    continue
        except Exception as e:
            print("Hirdetés megnyitási hiba:", e)
            break



def openAd(maxAds, sleepTime):
    global phone_type, location
    sleep(2)
    sponsored_present = False
    skipped_gpages = 0
    try:
        for i in range(3):
            if location == "m":
                if d(textContains="Szponzorált termékek").exists(timeout=2) or d(textContains="Szponzorált").exists(timeout=2):
                    sponsored_present = True
            if location == "r":
                if d(textContains="Produse sponsorizate").exists(timeout=2) or d(textContains="sponsorizate").exists(timeout=2):
                    sponsored_present = True
            if phone_type == "4g" and sponsored_present == False:
                d.swipe(550, 450, 550, 1000)
            if phone_type == "5g" and sponsored_present == False:
                d.swipe(360, 250, 360, 520)
            sleep(random.uniform(1,2))
        if sponsored_present == False:
            skipped_gpages += 1
        if sponsored_present == True:
            clickInstr(maxAds)
        sleep(random.uniform(1.5,3))
    except:
        print("Valami hiba történt az első lapon")
        sleep(random.uniform(1.5,3))
    try:
        if location == "m":
            d(text="Képek").click()
        if location == "r":
            d(text="Imagini").click()
        sponsored_present = False
        for i in range(3):
            if location == "m":
                if d(textContains="Szponzorált termékek").exists(timeout=2) or d(textContains="Szponzorált").exists(timeout=2):
                    sponsored_present = True
            if location == "r":
                if d(textContains="Produse sponsorizate").exists(timeout=2) or d(textContains="sponsorizate").exists(timeout=2):
                    sponsored_present = True
            if phone_type == "4g" and sponsored_present == False:
                d.swipe(550, 450, 550, 1000)
            if phone_type == "5g" and sponsored_present == False:
                d.swipe(360, 250, 360, 520)
            sleep(random.uniform(1,2))
        if sponsored_present == False:
            skipped_gpages += 1
        if sponsored_present == True:
            clickInstr(maxAds)
        sleep(random.uniform(1.5,3))
    except:
        print("'Képek' fül nem található")
        sleep(random.uniform(1.5,3))
    try:
        if location == "m":
            d(text="Termékek").click()
        if location == "r":
            d(text="Produse").click()
        sponsored_present = False
        for i in range(3):
            if location == "m":
                if d(textContains="Szponzorált termékek").exists(timeout=2) or d(textContains="Szponzorált").exists(timeout=2):
                    sponsored_present = True
            if location == "r":
                if d(textContains="Produse sponsorizate").exists(timeout=2) or d(textContains="sponsorizate").exists(timeout=2):
                    sponsored_present = True
            if phone_type == "4g" and sponsored_present == False:
                d.swipe(550, 450, 550, 1000)
            if phone_type == "5g" and sponsored_present == False:
                d.swipe(360, 250, 360, 520)
            sleep(random.uniform(1,2))
        if sponsored_present == False:
            skipped_gpages += 1
        if sponsored_present == True:
            clickInstr(maxAds)
        sleep(random.uniform(1.5,3))
    except:
        print("'Termékek' fül nem található")
        sleep(random.uniform(1.5,3))
    if skipped_gpages == 3:
        print(f"Timeout {sleepTime} mp-re")
        sleep(sleepTime)
        print(f"Letelt {sleepTime} mp")
        skipped_ads = 0


# Globális flag
clicked_homelux = False

def siteVisit():
    sleep(random.uniform(3,4))
    global clicked_homelux, phone_type

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
                if phone_type == "4g":
                    d.click(780, 800)
                if phone_type == "5g":
                    d.click(500, 570)
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
            if phone_type == "4g":
                d.swipe(540, 2000, 540, 370)
            if phone_type == "5g":
                d.swipe(360, 1330, 360, 280)
            sleep(random.uniform(0.5,2))
    else:
        sleep(random.uniform(2,5))

    d.press("back")


def close():
    d.press("home")
    d.shell("am force-stop com.android.chrome")


while Gstop == "False":
    readinFile()
    d = u.connect(f"127.0.0.1:{Gport}")
    for k in Gkeyword:
        airplaneMode(Gtime)
        os.system("curl ifconfig.me")
        print("\n")
        search(k)
        openAd(GmaxAd, Gshopstop)
        close()

