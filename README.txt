There are two types of programs in this directory.

For both cases, I should first start "ThermoTek\ThermoTekTCPServer_v1_00.py" and "V18\VerdiTCPServer_v1_00.py" to access the devices remotely. Make sure that both servers use correct serial ports. As long as there is no more USB-serial adapters with similar name, it won't be changed. If you added a lot of new USB-serial adapters and rebooted the server a few times, you need to find out which port gets assigned what name. (Still, this can be easily done by un-plugging and plugging-in the adapters.)

Main program is "MainWindow_v1_00.py" and it can be started either from inside Spyder or from command line. (It can be run with both python 3.5 and 3.6) To start it from command line, it is recommended to use "Anaconda Prompt". Check if the correct environment is selected by simply running 'python' and check the version number. If there is multiple environment with the same python version number, you can check the environment situation by running 'conda env list'. If you want to switch the environment, type 'activate environment_name'. As of Nov. 2017, all the root environment is installed with python 3.6.


Program inside "ruleCheck" is designed to monitor the system status periodically. For example, if the laser is on without chiller, ruleCheck will send a warning e-mail. For more details, check README.txt file inside "ruleCheck" directory.
