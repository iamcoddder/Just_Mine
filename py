import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = "Registration"
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 750
    page.window_resizable = True

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme)
            ],
            alignment=ft.MainAxisAlignment.CENTER
    ))

    def register(e):
        db = sqlite3.connect('egistr.r')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT            
        )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_password.value}')")

        db.commit()
        db.close()

        user_login.value = ''
        user_password.value = ''
        btn_reg.text = 'Added'
        page.update()

    def validate(e):
        if all([user_login.value, user_password.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
        if len(user_login.value) < 3:
            return
        if len(user_password.value) < 3:
            return

        page.update()

    def auth_user(e):
        db = sqlite3.connect('egistr.r')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_password.value}'")
        if cur.fetchone() != None:
            user_login.value = ''
            user_password.value = ''
            btn_auth.text = 'Authorized'

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationDestination(
                    icon=ft.icons.BOOK,
                    label='Account',
                    selected_icon=ft.icons.BOOKMARK
                ))

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Your data incorrect!"))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()

        user_login.value = ''
        user_password.value = ''
        btn_auth.text = 'Authorized'
        page.update()

    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_password = ft.TextField(label='Password', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Authorize', width=200, on_click=auth_user, disabled=True)

    # User Profile

    users_list = ft.ListView(spacing=10, padding=20)



    # User Profile end

    panel_register = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text('Registration'),
                        user_login,
                        user_password,
                        btn_reg
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Authorization'),
                    user_login,
                    user_password,
                    btn_auth
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_account = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Personal account'),
                    users_list
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0: page.add(panel_register)
        elif index == 1: page.add(panel_auth)
        elif index == 2:
            users_list.controls.clear()

            db = sqlite3.connect('egistr.r')

            cur = db.cursor()
            cur.execute(f"SELECT * FROM users")
            res = cur.fetchall()
            if res != None:
                for user in res:
                    users_list.controls.append(ft.Row([
                        ft.Text(f'User {user[1]}'),
                        ft.Icon(ft.icons.VERIFIED_USER_ROUNDED)
                    ]))
            db.commit()
            db.close()
            page.add(panel_account)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Registration"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label="Authorization")
        ], on_change=navigate
    )

    page.add(panel_register)


ft.app(target=main)
