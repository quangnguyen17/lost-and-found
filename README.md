
# Lost&Found
Powered by DojoAfterDark

"A missing item finder app that will help users find their glasses, keys, wallet, socks and other items that they put somewhere and then forget where they actually placed them. One way to do this is taking a pic with your phone each time you place such an item so that you can look at the pic if you forget about it later."

## Links

- [Live Site](https://lost.dojoafterdark.com)
- [Repo](https://github.com/quangnguyen17/lost-and-found)
- [Project Board](https://github.com/users/quangnguyen17/projects/1)
- [DojoAfterDark](https://dojoafterdark.com)
- Deployed using GitHub and [AWS](https://aws.amazon.com/).

## How to run the project locally

- Create a new project directory 
- `cd` to your that directory & run `python3 -m venv venv` to create a virtual environment
- Clone repo to your computer: `git clone https://github.com/quangnguyen17/lost-and-found.git`
- `cd` into repo folder
- `pip install -r requirements.txt` to install all the requirements to run project.
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- Finally, to start project, run this command: `python3 manage.py runserver` 
- Go to `http://localhost:8000/` on your browser and see the magic! :).
