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

def readinFile():
    os.system("rm config_07.txt")
    os.system("wget https://raw.githubusercontent.com/Nemethze/droidmatpuller/refs/heads/main/config_07.txt")
    try:
        with open("config_07.txt", "r") as file:
            lines = file.readlines()
    except:
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
    d.app_start("com.android.chrome")
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

spon_y = None
skipped_sites = 0

def openAd(maxAds, sleepTime):
    sleep(2)
    sponsored_present = False
    ads_opened = 0
    last_y = 0     
    skipped_ads = 0
    skipped_sites = 0
    while skipped_sites <= 2:
        if d(textContains="Produse sponsorizate").exists(timeout=2) or d(textContains="sponsorizate").exists(timeout=2):
            sponsored_present = True
            break
        if sponsored_present == False and skipped_sites<2:
            skipped_sites += 1
            d.swipe(550, 450, 550, 1000)
        if sponsored_present == False and skipped_sites==2:
            print(f"Timeout {sleepTime} mp-re")
            sleep(sleepTime)
            print(f"Letelt {sleepTime} mp")
            skipped_ads = 0
            break
    if sponsored_present == True:
        while ads_opened < maxAds and sponsored_present == True:
            try:
                blacklist_hit = False
                d.long_click(150, 1650, 2)
                sleep(random.uniform(2,3))
                d.click(540, 780)
                for b in Gblacklist:
                    if d(textContains=b).exists(timeout=0.5):
                        blacklist_hit = True
                        print(f" → Átugrom, mert blacklist találat: '{b}'")
                        blacklist_hit = True
                        d.click(1010, 2300)
                        sleep(random.uniform(0.5,1))
                        d.swipe(510, 1700, 155, 1700)
                        skipped_ads += 1
                        print(f"Átugrott hirdetések száma {skipped_ads}")
                        break
                if skipped_ads > 5:
                    print("Sok egymás utánni hirdetés")
                    break
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
                            d.click(900, 150)  # új fülre váltás
                            sleep(random.uniform(2,3))
                            d.click(830, 680)  # első katt az oldalon
                            sleep(random.uniform(2,3))
                            siteVisit()
                            sleep(random.uniform(2,3))
                            d.swipe(510, 1700, 163, 1700)  # görgetés
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


# Globális flag
clicked_homelux = False

def siteVisit():

    sleep(random.uniform(3,4))

    global clicked_homelux

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


while Gstop == "False":
    readinFile()
    print(Gstop)
    d = u.connect(f"127.0.0.1:{Gport}")
    for k in Gkeyword:
        airplaneMode(Gtime)
        os.system("curl ifconfig.me")
        search(k)
        openAd(GmaxAd, Gshopstop)
        close()
        
