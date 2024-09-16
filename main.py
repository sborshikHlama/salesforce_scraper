from modules.get_data_module import download_files
from modules.get_nps_module import download_nps
from modules.get_to2d_module import download_to2d
from datetime import datetime
import threading
from dotenv import load_dotenv
import os
from selenium.webdriver.support import expected_conditions as EC

cx_tixets_urls = [
    #"CX_GE_Tickets":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BBUA0/view",
    #"CX_FR_OFF":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BLUA0/view",
    #"CX_FR_ON":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BVUA0/view",
    #"CX_Expansions":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6rMUAS/view",
    #"CX_BE_Tickets": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BWUA0/view",
    #"CX_NL_Tickets":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BRUA0/view",
    #"CX_UK_Tickets":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BMUA0/view",
    #"BM_GE_Tickets":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BaUAK/view",
    #"CX_IT_Tickets":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6BNUA0/view"
]

csat_urls = [
    #"Reason_of_disat":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q3U0UAK/view",
    #"ALL_Main_Table":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q5nJUAS/view"
]

ar_urls = [
    #"AR_GE":
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q3StUAK/view",
    #"AR_FR": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q3SxUAK/view",
    #"AR_EXP": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q3SnUAK/view",
    #"AR_Appolo": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q4u4UAC/view",
    #"AR_NL2": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6yDUAS/view",
    #"AR_BE2": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q6y8UAC/view",
    #"AR_IT": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q5hBUAS/view",
    #"AR_UK": 
    "https://abinbev-ei-crm.lightning.force.com/lightning/r/Report/00O5I000001Q5wpUAC/view"
]

nps_url = "https://ambev.medallia.com/sso/ambev/applications/ex_WEB-9/pages/667?roleId=2811&f.pfug_abi_zone=65115&f.timeperiod=579&f.reporting-date=e_responsedate&alreftoken=%226528f377b6e39078debadc62f0045895%22&m.c309ce39-8f45-42c2-8dad-ea16aa83da6f.rows=%22e_abinbev_country_alt%22"

to2d_url = "https://abinbev-prod.eu-3.celonis.cloud/package-manager/ui/views/ui/spaces/c8bf44bd-2437-d5fd-8a08-84cda40aa013/packages/27d7cf6b-ea68-48a9-a589-0edf5f76980e/nodes/4a18dbca-7a04-49f5-806f-f448e1008dc6#!/documents/4a18dbca-7a04-49f5-806f-f448e1008dc6/view"

def main():
    """
    Executing download files function for all url lists.
    Params: void
    """
    # Get start time
    start_time = datetime.now()
    load_dotenv()

    username = os.getenv('USER')
    password = os.getenv('PASSWORD')

    username_nps = os.getenv('USER_NPS')
    password_nps = os.getenv('PASSWORD_NPS')

    cx_tickects_folder = os.getenv('CX_TICKETS_FOLDER')
    csat_folder = os.getenv('CSAT_FOLDER')
    ar_folder = os.getenv('AR_FOLDER')
    nps_folder = os.getenv('NPS_FOLDER')
    to2d_folder = os.getenv('TO2D_FOLDER')

    print('\033[96m' + "Downloading CX_Tickets....................................." + '\033[0m')
    # # download_files(cx_tixets_urls, username, password, cx_tickects_folder)
    t1 = threading.Thread(target=download_files, args=(cx_tixets_urls, username, password, cx_tickects_folder))
    print('\033[96m' + "Downloading CSAT..........................................." + '\033[0m')
    # # download_files(csat_urls, username, password, csat_folder)
    t2 = threading.Thread(target=download_files, args=(csat_urls, username, password, csat_folder,))
    print('\033[96m' + "Downloading Abandoned Rate................................." + '\033[0m')
    # # download_files(ar_urls, username, password, ar_folder)
    t3 = threading.Thread(target=download_files, args=(ar_urls, username, password, ar_folder))
    # # Start threads
    t1.start()
    t2.start()
    t3.start()

    # # Stop threads
    t1.join()
    t2.join()
    t3.join()

    # # download_nps(nps_url, username_nps, password_nps, nps_folder)
    # t4 = threading.Thread(target=download_nps, args=(nps_url, username_nps, password_nps, nps_folder))
    # # download_to2d(to2d_url, username_nps, password_nps, to2d_folder)
    # t5 = threading.Thread(target=download_to2d, args=(to2d_url, username_nps, password_nps, to2d_folder))
    
    # t4.start()
    # t5.start()

    # t4.join()
    # t5.join()

    print('\033[92m' + "FINISHED" + '\033[0m')
    # Get end time
    end_time = datetime.now()
    # Print how much time spent
    print("Download took:", end_time - start_time)

if __name__ == "__main__":
    main()