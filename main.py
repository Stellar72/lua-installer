DownloadLink = "https://unlimited.dl.sourceforge.net/project/luabinaries/5.3.6/Tools%20Executables/lua-5.3.6_Win64_bin.zip?viasf=1"

import requests
import zipfile
import os
import win32com.client
import ctypes
import time
import winreg
import shutil

TestingMode = False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if is_admin() == False and TestingMode == False:
    print("The executable must be ran as Administrator.")
    while True:
        time.sleep(60)

lua_folder_name = "lua536"

program_files = str.replace(os.environ.get('PROGRAMFILES')," (x86)","")

if os.path.exists(program_files+"\\"+lua_folder_name):
    answer = input("Do you want to uninstall lua 5.3.6? (y/n) \n> ")

    answer = str.lower(answer)

    if answer == "y" or answer == "yes" or answer == "yeah" or answer == "yup":
        try:
            lua_path = program_files+"\\"+lua_folder_name
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                                        0, winreg.KEY_ALL_ACCESS)
                value, reg_type = winreg.QueryValueEx(reg_key, 'Path')

                paths = value.split(';')
                if lua_path in paths:
                    paths.remove(lua_path)
                    new_value = ';'.join(paths)
                    winreg.SetValueEx(reg_key, 'Path', 0, reg_type, new_value)

                winreg.CloseKey(reg_key)

                os.system('setx PATH "{}" /M'.format(new_value))

            except OSError as e:
                print("ERROR WHEN MODIFYING REGISTRY: "+str(e))

            shutil.rmtree(lua_path,ignore_errors=True)
        except Exception as ex:
            print("err: "+str(ex))
        print("Lua succesfully uninstalled")
        while True:
            time.sleep(60)
    else:
        print("\nLua wont be uninstalled.")
        while True:
            time.sleep(60)
else:
    answer = str.lower(input("Do you want to install lua 5.3.6? (y/n)\n> "))

    if answer == "y" or answer == "yes" or answer == "yeah" or answer == "yup":
        print('Downloading lua 5.3.6')

        response = requests.get(DownloadLink)
        with open("lua.zip", 'wb') as file:
            file.write(response.content)


        print('Download complete, extracting lua.zip')

        with zipfile.ZipFile("lua.zip", 'r') as zip:
            zip.extractall(program_files+"\\"+lua_folder_name)

        os.remove("lua.zip")

        print('Extraction complete.')

        lua_path = program_files+"\\"+lua_folder_name

        os.rename(lua_path+"\\lua53.exe",lua_path+"\\lua.exe")

        print("You can find the lua folder at "+lua_path)

        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                        r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                                        0, winreg.KEY_ALL_ACCESS)

            value, reg_type = winreg.QueryValueEx(reg_key, 'Path')

            if lua_path not in value:
                new_value = value + ';' + lua_path
                winreg.SetValueEx(reg_key, 'Path', 0, reg_type, new_value)

            winreg.CloseKey(reg_key)
            os.system('setx PATH "{}" /M'.format(new_value))
        except PermissionError:
            print("You need to run this script as an administrator.")
        except Exception as e:
            print(f"Unexpected Error: {e}")

        seconds_to_close = 10

        print('\nLua Succesfully Installed. (Restart might be needed)\n\nClosing in '+str(seconds_to_close)+" seconds.")

        time.sleep(seconds_to_close)