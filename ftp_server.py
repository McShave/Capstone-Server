# Comment out the entire file to disable FTP functionality

# from pyftpdlib.authorizers import DummyAuthorizer
# from pyftpdlib.handlers import FTPHandler
# from pyftpdlib.servers import FTPServer
# import os
# import shutil
# import time

# FTP_DIRECTORY = "/home/pi/capstone_project/ftp_files"

# def cleanup_old_files(directory, max_age_days=7):
#     now = time.time()
#     for filename in os.listdir(directory):
#         file_path = os.path.join(directory, filename)
#         if os.stat(file_path).st_mtime < now - max_age_days * 86400:
#             os.remove(file_path)

# def start_ftp_server():
#     authorizer = DummyAuthorizer()
#     authorizer.add_user("user", "password", FTP_DIRECTORY, perm="elradfmw")
#     handler = FTPHandler
#     handler.authorizer = authorizer

#     server = FTPServer(("0.0.0.0", 21), handler)
#     print("[INFO] FTP server started.")
#     server.serve_forever()

# if __name__ == "__main__":
#     os.makedirs(FTP_DIRECTORY, exist_ok=True)
#     cleanup_old_files(FTP_DIRECTORY)
#     start_ftp_server()

