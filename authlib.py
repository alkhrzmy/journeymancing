import streamlit as st
import sqlite3 as sql


def auth(sidebar=True):

    try:
        conn = sql.connect("file:auth.db?mode=ro", uri=True)
    except sql.OperationalError:
        st.error(
            "Authentication Database is Not Found.\n\nConsider running authlib script in standalone mode to generate."
        )
        return None

    input_widget = st.sidebar.text_input if sidebar else st.text_input
    checkbox_widget = st.sidebar.checkbox if sidebar else st.checkbox
    user = input_widget("Username:")

    data = conn.execute("select * from users where username = ?", (user,)).fetchone()
    if user:
        password = input_widget("Enter Password:", type="password")
        if data and password == data[2]:
            if data[3]:
                if checkbox_widget("Check to edit user database"):
                    _superuser_mode()
            return user
        else:
            return None
    return None


def _list_users(conn):
    table_data = conn.execute("select username,password,names from users").fetchall()
    if table_data:
        table_data2 = list(zip(*table_data))
        st.table(
            {
                "Username": (table_data2)[0],
                "Password": table_data2[1],
                "Name": table_data2[2],
            }
        )
    else:
        st.write("No entries in authentication database")


def _create_users(conn, init_user="", init_pass="", init_super=""):
    user = st.text_input("Enter Username", value=init_user)
    pass_ = st.text_input("Enter Password (required)", value=init_pass)
    super_ = st.text_input("Enter Name", value=init_super)
    if st.button("Update Database") and user and pass_:
        with conn:
            conn.execute(
                "INSERT INTO USERS(username, password, names) VALUES(?,?,?)",
                (user, pass_, super_),
            )
            st.text("Database Updated")


def _edit_users(conn):
    userlist = [x[0] for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    edit_user = st.selectbox("Select user", options=userlist)
    if edit_user:
        user_data = conn.execute(
            "select username,password,names from users where username = ?", (edit_user,)
        ).fetchone()
        _create_users(
            conn=conn,
            init_user=user_data[0],
            init_pass=user_data[1],
            init_super=user_data[2],
        )


def _delete_users(conn):
    userlist = [x[0] for x in conn.execute("select username from users").fetchall()]
    userlist.insert(0, "")
    del_user = st.selectbox("Select user", options=userlist)
    if del_user:
        if st.button(f"Press to remove {del_user}"):
            with conn:
                conn.execute("delete from users where username = ?", (del_user,))
                st.write(f"User {del_user} deleted")


def _superuser_mode():
    with sql.connect("file:auth.db?mode=rwc", uri=True) as conn:
        conn.execute(
            "create table if not exists users (id INTEGER PRIMARY KEY, username UNIQUE ON CONFLICT REPLACE, password, names)"
        )
        mode = st.radio("Select mode", ("View", "Create", "Edit", "Delete"))
        {
            "View": _list_users,
            "Create": _create_users,
            "Edit": _edit_users,
            "Delete": _delete_users,
        }[mode](
            conn
        )  # I'm not sure whether to be proud or horrified about this...


if __name__ == "__main__":
    st.write(
        "Warning, superuser mode\n\nUse this mode to initialise authentication database"
    )
    if st.checkbox("Check to continue"):
        _superuser_mode()
