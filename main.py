from time import sleep
from os import makedirs, system
from os.path import exists
from sys import exit as sys_exit
from requests import get, session as requestsSession, ConnectionError, Timeout
from platform import system as os_name
from bs4 import BeautifulSoup as bs

from colorama import init, Fore, Style, Back
init(autoreset=True)

def throw_error(text:str):
    print("\n" + Back.RED + "FEJL")
    print(Fore.RED + text + "\n")
    while 1:
        try_again = input(Fore.RED + "Vil du forsøge igen? ja/nej: ")
        if try_again.lower() == "ja" or try_again.lower() == "nej":
            if try_again.lower() == "ja":
                print(Style.RESET_ALL)
                return main()
            else:
                sys_exit()
        else:
            print(Fore.RED + "Du skal svare med ja eller nej.")

def documents_in_folder(session, folder_url):
    sleep(1)
    resp = session.get(url=folder_url)
    return "Der kan ikke lægges dokumenter i denne mappe." not in resp.text and "Ingen tilgængelige dokumenter i mappen." not in resp.text

def download_documents(session, documents_url:str, folder_id:str, path:str):
    # Check if the folder has files, otherwise ignore
    if not documents_in_folder(session, f"{documents_url}&folderid={folder_id}"):
        return
    if not exists(path):
        makedirs(path)
    with session.get(url=f"{documents_url}&folderid={folder_id}", stream=True) as resp:
        soup = bs(resp.content, "html.parser")
        table_of_files = soup.find("div", {"id": "printfoldercontent"})
        table_of_files = table_of_files.find("table")
        table_elements = table_of_files.find_all("tr")
        for table_element in table_elements[1:]: # [1:] AKA start at index 1 in list
            try:
                file_element = table_element.find_all("td")[1]
                filename = file_element.a.text.strip().replace("/", "-")
                if filename.endswith("..."):
                    continue
                file_url = "https://www.lectio.dk" + file_element.a["href"]
                resp = session.get(url=file_url)
                with open(path+"/"+filename, "wb") as f:
                    f.write(resp.content)
                sleep(0.1)
            except Exception as e:
                #print(e)
                continue

def translate_subject_name(subject_name):
    subjects = {
        "fy": "Fysik",
        "ng": "Naturgeografi",
        "id": "Idræt",
        "da": "Dansk",
        "hi": "Historie",
        "ma": "Matematik",
        "ol": "Oldtidskundskab",
        "re": "Religion",
        "st": "Statistik",
        "en": "Engelsk",
        "ke": "Kemi",
        "tyb": "Tysk",
        "tyf": "Tysk",
        "me": "Mediefag",
        "ap": "Almen sprogforståelse",
        "nv": "Naturvidenskab",
        "sa": "Samfundsfag",
        "if": "Informatik",
        "as": "Astronomi",
        "bi": "Biologi",
        "bk": "Billedkunst",
        "bt": "Bioteknologi",
        "dr": "Dramatik",
        "eø": "Erhvervsøkonomi",
        "fi": "Filosofi",
        "fr": "Fransk",
        "frb": "Fransk",
        "frf": "Fransk",
        "it": "Italiensk",
        "ki": "Kinesisk",
        "la": "Latin",
        "mu": "Musik",
        "ps": "Psykologi",
        "sp": "Spansk",
    }
    subject = subject_name.split(" ")[1].lower()
    if subjects.get(subject[:-1]) != None:
        return subjects[subject[:-1]]
    if subjects.get(subject) != None:
        return subjects[subject]
    if len(subject) > 3:
        return subject.capitalize()
    return subject_name

def get_documents(username:str, password:str, school_id:int, download_activities:bool):
    # Login
    session = requestsSession()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"})
    login_url = f"https://www.lectio.dk/lectio/{school_id}/login.aspx"
    resp = session.get(url=login_url)
    soup = bs(resp.content, "html.parser")
    event_validation = soup.find_all("input", {"id": "__EVENTVALIDATION"})[0]["value"]
    try:
        school = soup.find_all("td", {"id": "m_Content_schoolnametd"})[0].getText()
    except IndexError:
        throw_error("Skole ID'et er ugyldigt.")
    form_data = {
        "__EVENTTARGET": "m$Content$submitbtn2",
        "__EVENTARGUMENT": "",
        "__EVENTVALIDATION": event_validation,
        "m$Content$username": username,
        "m$Content$password": password,
    }
    print(Fore.GREEN + "Logger ind...", end="\r")
    resp = session.post(url=login_url, data=form_data)
    if any(error_text in resp.text for error_text in ["Fejl i Brugernavn og/eller adgangskode", "Der er ikke oprettet en adgangskode til dette login"]):
        throw_error("Login fejlede, tjek om brugernavn, kodeord og skole ID er korrekt.")
    soup = bs(resp.content, "html.parser")
    name = soup.find_all("div", {"id": "s_m_HeaderContent_MainTitle"})[0].string.split(" ", 1)[1].split(",")[0]
    print(Fore.GREEN + "Logget ind som:")
    print(Fore.GREEN + "Elev:", name)
    print(Fore.GREEN + "Skole:", school+"\n")
    documents_url = "https://www.lectio.dk" + soup.find_all("a", {"id": "s_m_HeaderContent_subnavigator_ctl09"})[0]["href"]
    student_id = documents_url.split("elevid=")[1].split("&")[0]
    resp = session.get(url=documents_url)
    soup = bs(resp.content, "html.parser")
    options = soup.find("select", {"id": "s_m_ChooseTerm_term"})
    options = [int(option["value"]) for option in options.find_all("option")]
    terms = options[::-1]
    event_validation = soup.find_all("input", {"id": "__EVENTVALIDATION"})[0]["value"]
    if not exists("./LectioDownloads"):
        makedirs("./LectioDownloads")
    for n in range(0, len(options)):
        if n != 0:
            sleep(30) # Wait a little because of lectios internal rate limiting causing problems
        print(f"Begynder download af filer fra {n+1}. g ({terms[n]})...")
        viewstatex = soup.find_all("input", {"id": "__VIEWSTATEX"})[0]["value"]
        form_data = {
            "__EVENTTARGET": "s$m$ChooseTerm$term",
            "__EVENTVALIDATION": event_validation,
            "s$m$ChooseTerm$term": terms[n],
            "__VIEWSTATEX": viewstatex,
        }
        for x in range(0,16):
            resp = session.post(url=documents_url + f"&folderid=S{student_id}__2", data=form_data)
            if "Der opstod en ukendt fejl" in resp.text:
                if x == 15:
                    throw_error("En ukendt fejl opstod ved download.")
                else:
                    print(Fore.RED + "FEJL: Fildownload fejlede. Venter 25 sekunder og prøver igen...")
                    sleep(25)
                    continue
            else:
                break
        soup = bs(resp.content, "html.parser")
        treenode = soup.find("div", {"lec-node-id": "S"+student_id+"__2"})
        subjects_div = treenode.find("div", {"lec-role": "ltv-sublist"})
        subjects = subjects_div.find_all("div", {"lec-role": "treeviewnodecontainer"}, recursive=False)
        for subject in subjects:
            #subject_id = subject["lec-node-id"]
            subject_name = subject.find("div", {"class": "TreeNode-title"}).string
            subject_name = translate_subject_name(subject_name)
            sublist = subject.find("div", {"lec-role": "ltv-sublist"})
            sublist_trees = sublist.find_all("div", {"lec-role": "treeviewnodecontainer"}, recursive=False)

            for folder in sublist_trees:
                folder_name = folder.find("div", {"class": "TreeNode-title"}).string
                folder_id = folder["lec-node-id"]
                if folder_name == "Aktiviteter" and not download_activities:
                    continue

                # Now it's getting dirty, leave a PR if you have an easier and more elegant way to do this
                # Very messy, 2 girls 1 cup style
                sub_folders_in_folder = folder.find_all("div", {"lec-role": "treeviewnodecontainer"})
                if sub_folders_in_folder:
                    download_documents(session, documents_url, folder_id, f"./LectioDownloads/{terms[n]}/{subject_name}/{folder_name}")
                    for sub_folders in sub_folders_in_folder:
                        sub_folder_name = sub_folders.find("div", {"class": "TreeNode-title"}).string
                        sub_folder_id = sub_folders["lec-node-id"]
                        sub_sub_folders_in_folder = sub_folders.find_all("div", {"lec-role": "treeviewnodecontainer"})
                        if sub_sub_folders_in_folder:
                            download_documents(session, documents_url, sub_folder_id, f"./LectioDownloads/{terms[n]}/{subject_name}/{folder_name}/{sub_folder_name}")
                            for sub_sub_folders in sub_sub_folders_in_folder:
                                sub_sub_folder_name = sub_sub_folders.find("div", {"class": "TreeNode-title"}).string
                                sub_sub_folder_id = sub_sub_folders["lec-node-id"]
                                download_documents(session, documents_url, sub_sub_folder_id, f"./LectioDownloads/{terms[n]}/{subject_name}/{folder_name}/{sub_folder_name}/{sub_sub_folder_name}")
                        else:
                            download_documents(session, documents_url, sub_folder_id, f"./LectioDownloads/{terms[n]}/{subject_name}/{folder_name}/{sub_folder_name}")
                else:
                    download_documents(session, documents_url, folder_id, f"./LectioDownloads/{terms[n]}/{subject_name}/{folder_name}")

    input(Fore.GREEN + "Alle dokumenter er nu blevet downloaded! Filerne ligger inde i mappen \"LectioDownloads\". Ved at trykke på Enter, lukker du dette vindue.\nTak fordi du brugte dette program, jeg håber det virkede for dig og sparede dig en manuelt arbejde.")
    sys_exit()

def main():
    if os_name() == "Windows":
        system("cls")
    else:
        system("clear")
    try:
        splash_text = get(url="https://raw.githubusercontent.com/JC-Integrations/LectioDL/main/splash.txt")
    except (ConnectionError, Timeout) as exception:
        throw_error("Der er ikke forbindelse til internettet.")

    print(Fore.MAGENTA + splash_text.text + "\n")
    print(Fore.GREEN + "Nu skal du logge ind med samme oplysninger som du bruger til at logge ind på Lectio:\n")
    while 1:
        username = input("Brugernavn: ")
        if username == "":
            print(Fore.RED + "Du skal udfylde dette felt.")
        else:
            break
    while 1:
        password = input("Kodeord: ")
        if password == "":
            print(Fore.RED + "Du skal udfylde dette felt.")
        else:
            break
    print(Fore.GREEN + "\nFor at finde dit skole ID, skal du gå ind på Lectio og vælge din skole på login siden. Når den er valgt kan du se linket i toppen af din browser, her står dit skole ID, se eksemplet nedenunder.")
    print(Fore.GREEN + "https://www.lectio.dk/lectio/" + Back.RED + "93" + Style.RESET_ALL + Fore.GREEN + "/default.aspx")
    print(Fore.GREEN + "Her er skole ID'et 93.\n")

    while 1:
        try:
            school_id = int(input("Skole ID: "))
            break
        except:
            print(Fore.RED + "Du skal svare med et tal.")

    print()
    download_activities = False
    while 1:
        download_activities_input = input("Skal filer fra moduler downloades? ja/nej: ")
        if download_activities_input.lower() == "ja" or download_activities_input.lower() == "nej":
            if download_activities_input.lower() == "ja":
                download_activities = True
            break
        else:
            print(Fore.RED + "Du skal svare med ja eller nej.")
    print()

    get_documents(username, password, school_id, download_activities)

if __name__ == "__main__":
    main()