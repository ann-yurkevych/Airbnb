import psycopg2
from AirBnb import db_connect


def max_reservations(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT G.name, G.id
                FROM Guests G
                JOIN (
                    SELECT guest_id, COUNT(*) AS reservation_count
                    FROM Reservation
                    GROUP BY guest_id
                    ORDER BY reservation_count DESC
                    LIMIT 1
                ) AS R
                ON G.id = R.guest_id;
                """
            )
            result = cursor.fetchone()
            if result:
                username, user_id = result
                print(
                    f"The user with the most reservations is {username} (User ID: {user_id})"
                )
            else:
                print("No user found.")
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to find the user with the most reservations")
        print(e)


if __name__ == "__main__":
    conn = db_connect()
    with conn.cursor() as cursor:
        try:
            cursor.execute(max_reservations(conn))
            user = cursor.fetchone()
            print("User with max reservations", user)
        except Exception as e:
            print("Error:", e)
