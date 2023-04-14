ruleViolationCheck_v1_00.py is designed to be called by cron job. To add this to a cron, type "crontab -e". This will open one of the text editor. Inside the crontab, add a line similar to the next one:

* * * * * /usr/bin/python3 /home/pi/MiraControl/ruleCheck/ruleViolationCheck_v1_00.py

Do not use "ruleViolationCheck_v1_00_DEBUG.py" for cron job because it will print out many information, and cron send you an internal e-mail whenever there is any output from any cron job.

Whenever ruleViolationCheck_v1_00.py finds out any rule violation, it will create some flag file inside flags directory. Important purpose of flag files is to prevent multiple error e-mails for the same problem. Also flag file will be automatically removed once the problem is gone. However, if the same problem continues to exist, it won't send any extra e-mail.

