"Secretum" is a terminal-based password manager software written in Python, designed specifically for Ubuntu OS. It provides a secure and convenient way to store and manage all your passwords and sensitive information. With Secretum, you can generate strong, unique passwords, store them in an encrypted database, and access them easily from the command line interface. It offers features such as password generation, password strength analysis, search, and copy-to-clipboard functionality. Secretum uses the latest encryption algorithms to ensure that your data is kept safe and secure. Take control of your passwords with Secretum and never worry about forgetting or losing them again.
---
Features:
    Secure Storage: Passwords should be securely stored, perhaps using encryption or hashing to ensure that they cannot be accessed by unauthorized parties.

    Password Generation: Include a password generator that can create strong, randomized passwords that are difficult to guess.

    User Authentication: You could require the user to authenticate themselves with a master password before accessing the password manager. This would help prevent unauthorized access to their stored passwords.

    Password Entry and Retrieval: Allow users to add, edit, and delete their stored passwords. They should also be able to easily retrieve their stored passwords when needed.

    User Interface: Develop a simple and easy-to-use terminal-based user interface that allows users to interact with the application and manage their passwords.

    Backup and Restore: Provide an option to backup and restore password data in case of a system failure or other unforeseen circumstances.

    Multi-Platform Compatibility: Ensure that the application is compatible with multiple operating systems, including Ubuntu and other Linux distributions.

These are just a few potential features for your password manager terminal application. You could also consider adding additional features, such as password expiration reminders or the ability to categorize and sort passwords. Good luck with your project!

Project Secretum is a GUI based password managing application.

The program initializes by first asking the user for a name, a password and confirmation, and an e-mail address to create an empty encrypted CSV file under /home/$user/.config/secretum directory.

After signing up, every time the program is started the user has 3 entries to enter the correct password or else the program logs a breach failure report and automatically sends it to the e-mail address provided by the user (which can also be changed from the setting).

The GUI is a thin window with a service list on bottom and an empty space on top of it to display the password upon clicking the service's name or icon.

The application has an automatically closing function which can be altered in the settings by user. Also, the user can change the current password within the setting. 

Secretum also provides an export function for one, multiple, or all passwords and an appending function for one service and password.
