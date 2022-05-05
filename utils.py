from aiogram.utils.helper import Helper, HelperMode, ListItem


class UserState(Helper):
    mode = HelperMode.snake_case

    USER_STATE = ListItem()
    MAP_STATE = ListItem()



if __name__ == '__main__':
    print(UserState.all())