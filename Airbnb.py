import psycopg2


def db_connect():
    try:
        host = "localhost"
        dbname = "postgres"
        user = "postgres"
        password = "1111"
        port = "5432"

        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
        )
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database")
        print(e)
    return conn


def db_create_tables(conn):
    try:
        create_table_queries = [
            """
            CREATE TABLE Guests (
                id serial PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(255)  NOT NULL,
                credit_card INT NOT NULL UNIQUE
            );
            """,
            """
            CREATE TABLE Hosts (
                id serial PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(255) NOT NULL,
                rating REAL NOT NULL
            );
            """,
            """
            CREATE TABLE Rooms (
                id serial PRIMARY KEY,
                host_id INT NOT NULL,
                price INT NOT NULL,
                capacity INT NOT NULL,
                type_of_allocation VARCHAR(255) NOT NULL,
                housing_type VARCHAR(255) NOT NULL,
                facilities VARCHAR(255) NOT NULL,
                amount_of_beds INT NOT NULL,
                amount_of_bathrooms INT NOT NULL,
                FOREIGN KEY (host_id) REFERENCES Hosts(id)
            );
            """,
            """
            CREATE TABLE Reservation (
                id serial PRIMARY KEY,
                guest_id INT NOT NULL,
                room_id INT NOT NULL,
                price INT NOT NULL,
                FOREIGN KEY (guest_id) REFERENCES Guests(id),
                FOREIGN KEY (room_id) REFERENCES Rooms(id)
            );
            """,
            """
            CREATE TABLE Reviews (
                id serial PRIMARY KEY,
                guest_id INT NOT NULL,
                host_id INT NOT NULL,
                room_id INT NOT NULL,
                rating_guest REAL NOT NULL UNIQUE,
                comment TEXT NOT NULL,
                FOREIGN KEY (guest_id) REFERENCES Guests(id),
                FOREIGN KEY (host_id) REFERENCES Hosts(id),
                FOREIGN KEY (room_id) REFERENCES Rooms(id)
            );
            """,
            """
            CREATE TABLE Payment (
                id serial PRIMARY KEY,
                guest_id INT NOT NULL,
                reservation_id INT NOT NULL,
                type_of_payment VARCHAR(255) NOT NULL,
                guest_card INT NOT NULL,
                FOREIGN KEY (guest_id) REFERENCES Guests(id),
                FOREIGN KEY (reservation_id) REFERENCES Reservation(id)
            );
            """,
        ]

        with conn.cursor() as cursor:
            for query in create_table_queries:
                cursor.execute(query)
            conn.commit()

        print("Tables created successfully!")
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to create tables")
        print(e)
        # print(query)


def insert_guest(conn, name, email, password, phone, credit_card):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Guests (name, email, password, phone, credit_card)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (name, email, password, phone, credit_card),
            )
            guest_id = cursor.fetchone()[0]
            conn.commit()
            return guest_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Guests table")
        print(e)


def insert_host(conn, name, email, password, phone, rating):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Hosts (name, email, password, phone, rating)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (name, email, password, phone, rating),
            )
            host_id = cursor.fetchone()[0]
            conn.commit()
            return host_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Hosts table")
        print(e)


def insert_room(
    conn,
    host_id,
    price,
    capacity,
    type_of_allocation,
    housing_type,
    facilities,
    amount_of_beds,
    amount_of_bathrooms,
):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Rooms (host_id, price, capacity, type_of_allocation, housing_type, facilities, amount_of_beds, amount_of_bathrooms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    host_id,
                    price,
                    capacity,
                    type_of_allocation,
                    housing_type,
                    facilities,
                    amount_of_beds,
                    amount_of_bathrooms,
                ),
            )
            room_id = cursor.fetchone()[0]
            conn.commit()
            return room_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Rooms table")
        print(e)


def insert_reservation(conn, guest_id, room_id, price):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Reservation (guest_id, room_id, price)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (guest_id, room_id, price),
            )
            reservation_id = cursor.fetchone()[0]
            conn.commit()
            return reservation_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Reservation table")
        print(e)


def insert_review(conn, guest_id, host_id, room_id, rating_guest, comment):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Reviews (guest_id, host_id, room_id, rating_guest, comment)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (guest_id, host_id, room_id, rating_guest, comment),
            )
            review_id = cursor.fetchone()[0]
            conn.commit()
            return review_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Reviews table")
        print(e)


def insert_payment(conn, guest_id, reservation_id, type_of_payment, guest_card):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Payment (guest_id, reservation_id, type_of_payment, guest_card)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (guest_id, reservation_id, type_of_payment, guest_card),
            )
            payment_id = cursor.fetchone()[0]
            conn.commit()
            return payment_id
    except (psycopg2.Error, Exception) as e:
        print("Error: Unable to insert data into Payment table")
        print(e)


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
    # db_create_tables(conn)
    guest_id = insert_guest(
        conn, "Drabchuk Ha", "drabchukw@gmail.com", "1113", "0001", 1236
    )
    host_id = insert_host(
        conn, "Yurkevych Yo", "yurkevych@gmail.com", "1111", "0000", 4.5
    )
    room_id = insert_room(
        conn, host_id, 100, 2, "Private", "Apartment", "Wi-Fi", 2, 1
    )
    reservation_id = insert_reservation(conn, guest_id, room_id, 100)
    review_id = insert_review(conn, guest_id, host_id, room_id, 4.5, "Love this!")
    payment_id = insert_payment(conn, guest_id, reservation_id, "Master Card", 1234)

    select_query = "SELECT * FROM Rooms;"  # from choosen table
    with conn.cursor() as cursor:
        conn.rollback()

        cursor.execute(select_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
