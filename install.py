
import os
import subprocess

""" => Notes =============================================================================================

# ! ALERT: wheel (and setuptools) must be installed so that an egg-link file is made
    # ! "C:/Users/kclar/AppData/Local/Programs/Python/Python312/Lib/site-packages/mygame.egg-link"
    # ** THIS IS ABSOLUTELY ESSENTIAL FOR PYLANCE TO RECOGNISE IMPORTS

=> =================================================================================================== """

# try:
#     import wheel
# except ImportError:
#     print("Error: The 'wheel' package is not installed.")
#     print("Please install it using: pip install wheel")
#     exit(1)

# ~ Change the working directory to the script's directory
os.system('cls')
print('Running install.py')
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def install(editable):
    """Function to install the package"""
    if editable:
        subprocess.run(["pip", "install", "-e", "."])
    else:
        subprocess.run(["pip", "install", "."])

def question():
    """Function to prompt for user confirmation and optionally install the package"""
    while True:
        choice = input(f"Directory: {script_dir}\nWould you like to update the package from this directory (Y/N)? ").strip().lower()
        if choice == "y":
            while True:
                choice = input(f"Would you like to install in editable mode or regular (E/R)? ").strip().lower()
                if choice == "e":
                    print('Installing the pacakge in editable mode, __.egg-link added to site-packages.')
                    install(editable = True)
                    break
                elif choice == 'r':
                    print('Installing the pacakge in regular mode, all files added to site-packages')
                    install(editable = False)
                    break
                else:
                    print("Invalid choice. Please enter E for editable or r for regular.")
            break
        elif choice == "n":
            print("Not updating the package, exiting.")
            break
        else:
            print("Invalid choice. Please enter Y for Yes or N for No.")

# ~ Call the question function
question()
