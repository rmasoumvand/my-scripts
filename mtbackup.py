import ftplib
import logging
import os
from datetime import date

logging.basicConfig(filename="D:\\log.txt", level=logging.DEBUG, format="%(asctime)s [%(levelname)5s] %(message)s", datefmt='%Y/%m/%d %I:%M:%S %p')

TODAY = date.today().strftime("%m-%d-%Y")
BACKUP_PATH=f"D:\\Mikrotik Backups\\{TODAY}"

FTP_HOST = ("","","")
FTP_USER = ""
FTP_PASS = ""
FTP_PORT = 21
FTP_FILENAME = ""

if not os.path.isdir(BACKUP_PATH):
    logging.info(f"Creating Backup directory {BACKUP_PATH}")
    os.makedirs(BACKUP_PATH)
for host in FTP_HOST:
    try:
        logging.info(f"Connecting to {host}")
        ftp = ftplib.FTP()
        ftp.connect(host, FTP_PORT)
        logging.info(f"Logging with user {FTP_USER}")
        ftp.login(FTP_USER, FTP_PASS)

        with open(f"{BACKUP_PATH}\\Backup {host} {TODAY}.bak", "wb") as file:
            logging.info(f"Getting {FTP_FILENAME}")
            ftp.retrbinary(f"RETR {FTP_FILENAME}", file.write)
    except Exception as e:
        logging.error(e)
    finally:
        if ftp is not None:
            logging.info(f"Closing connection for {host}")
            ftp.close()
