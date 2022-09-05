# import os
#
# file_path = "./vc"
#
# # checking whether file exists or not
# if os.path.exists(file_path):
#     # removing the file using the os.remove() method
#     os.remove(file_path)
# else:
#     # file not found message
#     print("File not found in the directory")
#
# file_path = "./courseScreenShot"
#
# # checking whether file exists or not
# if os.path.exists(file_path):
#     # removing the file using the os.remove() method
#     os.remove(file_path)
# else:
#     # file not found message
#     print("File not found in the directory")

import shutil
import os.path

if os.path.exists("../vc"):
    shutil.rmtree("../vc")
if os.path.exists("../courseScreenShot"):
    shutil.rmtree("../courseScreenShot")