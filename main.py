from repository import *
print("Welcome to store!")
while True:
    try:
        symbol = int(input("What do you wanna do?\n1.Add client\n2.Show clients\n3.Delete client\n4.Add product\n5.Show products\n6.Delete product\n7.Make order\n8.Show orders\n9.Delete order\n10.Report\n11.Exit\n: "))
    except ValueError:
        print("There's no such an option!")
    match symbol:
        case 1:
            add_client()
        case 2:
            show_clients()
        case 3:
            delete_client()
        case 4: 
            add_product()
        case 5:
            show_products()
        case 6:
            delete_product()
        case 7: 
            make_order()
        case 8:
            show_orders()
        case 9:
            delete_order()
        case 10:
            report()
        case 11:
            print("Goodbye!")
            break
    while True:
        input("Press any key to continue...")
        break

