def file_exists(file_name):
    try:
        with open(file_name, "r"):
            return True
    except FileNotFoundError:
        return False

def save_product_catalog(product_catalog, file_name):
    with open(file_name, "w") as file:
        for product, price in product_catalog.items():
            file.write(f"{product}:{price}\n")

def load_product_catalog(file_name):
    product_catalog = {}
    try:
        with open(file_name, "r") as file:
            for line in file:
                product, price = line.strip().split(":")
                product_catalog[product] = float(price)
    except FileNotFoundError:
        pass
    return product_catalog

def save_users(users):
    with open("users.txt", "w") as file:
        for username, password in users:
            file.write(f"{username}:{password}\n")

def load_users():
    users = []
    try:
        with open("users.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                users.append((username, password))
    except FileNotFoundError:
        pass
    return users

def save_admin_credentials(admin_username, admin_password):
    with open("admin.txt", "w") as file:
        file.write(f"{admin_username}:{admin_password}\n")

def load_admin_credentials():
    try:
        with open("admin.txt", "r") as file:
            admin_username, admin_password = file.readline().strip().split(":")
    except FileNotFoundError:
        admin_username = "Admin"
        admin_password = "Admin"
        save_admin_credentials(admin_username, admin_password)
    return admin_username, admin_password

def save_admin_product_catalog(admin_product_catalog):
    with open("admin_product_catalog.txt", "w") as file:
        for product, price in admin_product_catalog.items():
            file.write(f"{product}:{price}\n")

def load_admin_product_catalog():
    admin_product_catalog = {}
    try:
        with open("admin_product_catalog.txt", "r") as file:
            for line in file:
                product, price = line.strip().split(":")
                admin_product_catalog[product] = float(price)
    except FileNotFoundError:
        pass
    return admin_product_catalog

def login(username, password, users):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

def main():
    # Створити файли з початковими даними, якщо вони не існують
    if not file_exists("product_catalog.txt"):
        save_product_catalog({
            "headphone": 4000,
            "charge": 500,
            "TV": 40000,
            "iphone": 20000,
            "android": 15800,
            "laptop": 36000
        }, "product_catalog.txt")

    if not file_exists("admin_product_catalog.txt"):
        save_product_catalog({}, "admin_product_catalog.txt")

    if not file_exists("users.txt"):
        save_users([])

    if not file_exists("admin.txt"):
        save_admin_credentials("Admin", "Admin")

    product_catalog = load_product_catalog("product_catalog.txt")
    admin_product_catalog = load_product_catalog("admin_product_catalog.txt")

    users = load_users()
    admin_username, admin_password = load_admin_credentials()
    cart = []
    current_user = None

    while True:
        print("\nМеню:")
        print("1. Реєстрація")
        print("2. Увійти як адміністратор")
        print("3. Переглянути каталог продуктів")
        print("4. Додати продукт до кошика")
        print("5. Придбати товари")
        print("6. Вийти")
        print("7. Увійти")
        print("8. Додати продукт до адмінського каталогу (тільки для адміністратора)")
        choice = input("Оберіть опцію: ")

        if choice == "1":
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            users.append((username, password))
            save_users(users)
            current_user = (username, password)
            print("Реєстрація успішна.")

        elif choice == "2":
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            if username == admin_username and password == admin_password:
                current_user = (username, password)
                print("Успішно увійшли як адміністратор.")
            else:
                print("Невірний логін або пароль.")

        elif choice == "3":
            print("\nКаталог продуктів:")
            for product, price in product_catalog.items():
                print(f"{product}: {price} грн")

        elif choice == "4":
            if not current_user:
                print("Спершу увійдіть у систему.")
            else:
                product_name = input("Введіть назву продукту, який додаєте в кошик: ")
                if product_name in product_catalog:
                    quantity = int(input(f"Введіть кількість '{product_name}' товару: "))
                    cart.append((product_name, product_catalog[product_name], quantity))
                    print(f"{quantity} одиниць '{product_name}' додано до кошика.")
                else:
                    print("Продукт не знайдено в каталозі.")

        elif choice == "5":
            if not current_user:
                print("Спершу увійдіть у систему.")
            elif not cart:
                print("Кошик порожній.")
            else:
                total_price = sum(item[1] * item[2] for item in cart)
                print(f"Загальна сума до оплати: {total_price} грн")
                cart = []

        elif choice == "6":
            print("До побачення!")
            break

        elif choice == "7":
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            if login(username, password, users):
                current_user = (username, password)
                print("Успішний вхід.")
            else:
                print("Користувач не зареєстрований. Бажаєте зареєструватись? (Yes/No)")
                register_choice = input()
                if register_choice.lower() == "yes":
                    new_username = input("Введіть новий логін: ")
                    new_password = input("Введіть новий пароль: ")
                    users.append((new_username, new_password))
                    save_users(users)
                    current_user = (new_username, new_password)
                    print("Реєстрація успішна.")
                else:
                    print("До побачення!")

        elif choice == "8" and current_user and current_user[0] == admin_username:
            new_product_name = input("Введіть назву нового продукту для адмінського каталогу: ")
            new_product_price = float(input("Введіть ціну для нового продукту: "))
            admin_product_catalog[new_product_name] = new_product_price
            save_product_catalog(admin_product_catalog, "admin_product_catalog.txt")
            print(f"Продукт '{new_product_name}' додано до адмінського каталогу.")

        else:
            print("Невірний вибір. Спробуйте ще раз.")

    save_product_catalog(product_catalog, "product_catalog.txt")

if __name__ == "__main__":
    main()