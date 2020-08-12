from tkinter import *
import mysql.connector
from PIL import Image, ImageTk
from functools import partial
import locale
from datetime import datetime
#from notify_run import Notify
import random
import webbrowser
from tkinter import messagebox


class TheGanges:
    def __init__(self, win, *args, **kwargs):
        self.mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = # enter password of mysql,
            database = 'the_ganges'
        )

        self.mycursor = self.mydb.cursor()

        reset_id = """
                        ALTER TABLE products_info
                        DROP COLUMN id;

                        ALTER TABLE products_info
                        ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY;

                """
        self.mycursor.execute(reset_id, multi = True)

        self.win = win
        self.win.wm_state('zoomed') 
        self.win.title('The Ganges')
        self.win.config(bg = 'Ghost white')

        #self.notify = Notify()
        self.coupon_code = None

        self.current_id = None
        self.option_variable = StringVar()
        self.search_name = ""
        self.if_logged_in = False
        self.but_button = None
        self.login_frame = Frame()
        self.username_entry = Entry()
        self.password_entry = Entry()
        self.new_password_entry = Entry()
        self.new_username_entry = Entry()
        self.last_name_entry = Entry()
        self.entry_name = Entry()
        self.phone_no_entry = Entry()
        self.register_frame = Frame()
        self.product_id = 0
        self.quantity_option_menu = None
        self.quantity_entry = Entry()
        self.allow_quantity = 'no'
        self.main_product_frame = Frame()
        self.user_id = 0
        self.add_to_cart_scr = None
        self.stay_signed = False
        self.yes = "no"
        self.view_cart_canvas = Canvas()
        self.view_cart_var = StringVar()
        self.product_display_frame = Frame()
        self.view_cart_scr = None
        self.view_cart_button = Button()
        self.logo_image = None
        self.names_tuple = []
        self.search_entry = Entry()
        self.search_button = Button()
        self.view_account_button = Button()
        self.main_outer_frame = Frame()
        self.main_scr_frame = Frame()
        self.main_scr_canvas = Canvas()
        self.my_scrollbar = Scrollbar()
        self.view_profile_button = Button()
        self.view_points_button = Button()
        self.pass_count = 0
        self.otp = 1
        self.enter_otp_entry = Entry()
        self.if_otp_true = False
        self.view_profile_scr = None
        self.get_otp_frame = Frame()
        self.first_name_entry = Entry()
        self.account_detail_scr = None
        self.points = 0
        self.view_order_button = Button()
        self.order_scr_canvas = Canvas()
        self.status = None
        self.payment_mode = "Cash On Delivery(COD)"
        self.checkout_scr = None
        self.radio_var = StringVar()
        self.expiry_var = IntVar()
        self.checkout_frame = Frame()
        self.total_product_amount = 0
        self.subtotal_str = None
        self.bank_name = None
        self.get_coupon_button = None
        self.subtotal = 0
        self.discount_eligible = False

        self.main_menu()

    def log_out(self, scr):
        scr.destroy()
        remove_signed_in = """
                        UPDATE users_info
                        SET if_signed_in = FALSE
                        WHERE id = %s
        """
        self.mycursor.execute(remove_signed_in, (self.user_id, ))
        self.mydb.commit()
        self.if_logged_in = False
        self.view_account_button.destroy()
        self.win.after(0, self.main_menu)

    def main_menu(self):
        view_cart_image = Image.open("view_cart.png")
        view_cart_image_size = (170, 75)
        view_cart_image = view_cart_image.resize(view_cart_image_size)
        view_cart_render = ImageTk.PhotoImage(view_cart_image)

        self.view_cart_button = Button(self.win, image = view_cart_render, bd = 0, bg = 'ghost white')
        self.view_cart_button.configure(activebackground = 'ghost white', command = self.view_cart)

        self.view_cart_button.image = view_cart_render
        self.view_cart_button.place(x = 1170, y = 15)

        logo_size = (400, 100)
        self.logo_image = Image.open('shop_logo.PNG')
        self.logo_image = self.logo_image.resize(logo_size)
        logo_render = ImageTk.PhotoImage(self.logo_image)

        logo_label = Label(self.win, image = logo_render, bg = 'Ghost White')
        logo_label.image = logo_render
        logo_label.place(x = 0, y = 0)

        list_of_names = []

        get_names = "SELECT product_name FROM products_info"
        self.mycursor.execute(get_names)
        self.names_tuple = self.mycursor.fetchall()  # stores result

        for self.names in self.names_tuple:
            list_of_names.append(str(self.names[0]))

        self.search_entry = DisplaySuggestion(list_of_names, self.win)
        self.search_entry.config(font = ('arial', 21))
        self.search_entry.place(x = 500, y = 30)

        search_button_size = (35, 35)
        search_button_image = Image.open('search_pic.PNG')
        search_button_image = search_button_image.resize(search_button_size)
        search_button_render = ImageTk.PhotoImage(search_button_image)

        self.search_button = Button(self.win, image = search_button_render, bd = 0, command = self.search_item)
        self.search_button.image = search_button_render
        self.search_button.place(x = 820, y = 30)

        get_signed_in_user = "SELECT id FROM users_info WHERE if_signed_in = TRUE"
        self.mycursor.execute(get_signed_in_user)
        signed_in_user_stage2 = self.mycursor.fetchall()
        if len(signed_in_user_stage2) != 0:
            signed_in_user = signed_in_user_stage2[0]
            self.user_id = signed_in_user[0]
            self.if_logged_in = True

        self.view_account_button = Button(self.win)
        if self.if_logged_in:
            get_user_name = "SELECT first_name FROM users_info WHERE id = %s"
            self.mycursor.execute(get_user_name, (self.user_id,))
            user_name_stage2 = self.mycursor.fetchall()
            user_name_stage1 = user_name_stage2[0]
            user_name = "Hello " + user_name_stage1[0] + ", \n view account"
            self.view_account_button.config(command = self.account_details, text = user_name, font = (None, 13))
        else:
            not_logged_in = "Log In to view\n account details"
            self.view_account_button.config(command = lambda: self.default_login("view_account"), text = not_logged_in,
                                            font = (None, 20 - 7))
        self.view_account_button.place(x = 1000, y = 25)

        self.main_outer_frame = Frame(root)
        self.main_outer_frame.place(x = 1, y = 100)

        self.main_scr_canvas = Canvas(self.main_outer_frame)
        self.main_scr_frame = Frame(self.main_scr_canvas)
        self.main_scr_frame.pack()
        self.my_scrollbar = Scrollbar(self.main_outer_frame, orient = "vertical", command = self.main_scr_canvas.yview)
        self.main_scr_canvas.configure(yscrollcommand = self.my_scrollbar.set)

        self.my_scrollbar.pack(side = "right", fill = "y")
        self.main_scr_canvas.pack()
        self.main_scr_canvas.create_window((0, 0), window = self.main_scr_frame)

        self.main_scr_frame.bind("<Configure>", self.inner_frame_binder)
        self.main_scr_canvas.bind_all("<MouseWheel>", self.scroll_canvas)

        self.place_products()
        self.search_entry.bind("<BackSpace>", self.backspace_pressed)

    def resend_otp(self):
        self.otp = random.randint(10000, 99999)
        self.notify.send('Your OTP is ' + str(self.otp))

    def view_profile(self):
        self.view_profile_scr = Toplevel(self.account_detail_scr)
        self.view_profile_scr.wm_state('zoomed')
        self.view_profile_scr.title('VIEW PROFILE')

        logo_image = ImageTk.PhotoImage(self.logo_image)
        logo_label = Label(self.view_profile_scr, image = logo_image)
        logo_label.image = logo_image
        logo_label.place(x = 0, y = 0)
        if not self.if_otp_true:
            self.get_otp_frame = Frame(self.view_profile_scr, bd = 8, relief = RIDGE, height = 300, width = 400)
            self.get_otp_frame.place(x = 500, y = 200)

            otp_frame_head = Label(self.view_profile_scr, text = "OTP sent on 9990******", font = (None, 20))
            otp_frame_head.place(x = 500, y = 160)

            self.otp = random.randint(10000, 99999)

            self.notify.send('your OTP is ' + str(self.otp))

            enter_otp_label = Label(self.get_otp_frame, text = "Enter OTP:", font = (None, 20))
            enter_otp_label.place(x = 0, y = 20)

            self.enter_otp_entry = Entry(self.get_otp_frame, font = (None, 20))
            self.enter_otp_entry.place(x = 30, y = 100)

            resend_otp = Button(self.get_otp_frame, text = "Resend OTP", fg = 'blue2', bd = 0,
                                activeforeground = 'blue2', command = self.resend_otp)
            resend_otp.place(x = 40, y = 150)

            submit_otp = Button(self.get_otp_frame, text = 'Check', font = (None, 15), bg = 'DarkOrange1',
                                command = self.check_otp, padx = 20, pady = 10)
            submit_otp.place(x = 100, y = 200)
        elif self.if_otp_true:

            profile_frame = Frame(self.view_profile_scr, width = 1300, height = 600, bd = 12, relief = SUNKEN)
            profile_frame.place(x = 0, y = 100)

            get_details = "SELECT first_name, second_name, username, password, phone_no FROM users_info WHERE id = %s"
            self.mycursor.execute(get_details, (self.user_id,))

            details_stage2 = self.mycursor.fetchall()
            details = details_stage2[0]

            first_name_label = Label(profile_frame, text = 'First Name ', font = (None, 25))
            last_name_label = Label(profile_frame, text = "Last Name ", font = (None, 25))
            phone_no_label = Label(profile_frame, text = "Phone No. ", font = (None, 25))
            username_label = Label(profile_frame, text = "Username ", font = (None, 25))
            password_label = Label(profile_frame, text = "Password ", font = (None, 25))

            first_name_label.place(x = 0, y = 20)
            last_name_label.place(x = 0, y = 120)
            phone_no_label.place(x = 0, y = 220)
            username_label.place(x = 0, y = 320)
            password_label.place(x = 0, y = 420)

            self.first_name_entry = Entry(profile_frame, font = (None, 25))
            self.last_name_entry = Entry(profile_frame, font = (None, 25))
            self.phone_no_entry = Entry(profile_frame, font = (None, 25))
            self.username_entry = Entry(profile_frame, font = (None, 25))
            self.password_entry = Entry(profile_frame, font = (None, 25), show = "●")

            self.first_name_entry.insert(0, details[0])
            self.last_name_entry.insert(0, details[1])
            self.username_entry.insert(0, details[2])
            self.password_entry.insert(0, details[3])
            self.phone_no_entry.insert(0, details[4])

            self.first_name_entry.place(x = 250, y = 20)
            self.last_name_entry.place(x = 250, y = 120)
            self.phone_no_entry.place(x = 250, y = 220)
            self.username_entry.place(x = 250, y = 320)
            self.password_entry.place(x = 250, y = 420)

            eye_image = Image.open("show_pass.png")
            eye_image_size = (55, 25)
            eye_image = eye_image.resize(eye_image_size)
            eye_render = ImageTk.PhotoImage(eye_image)

            eye_button = Button(profile_frame, image = eye_render, bg = 'white', bd = 0,
                                activebackground = 'white', command = self.show_pass)
            eye_button.image = eye_render
            eye_button.place(x = 560, y = 427)

            update_button = Button(profile_frame, text = "Update Credentials", font = (None, 20), bg = 'DarkOrange1',
                                   command = self.update_cred)
            update_button.place(x = 900, y = 200)

    def update_cred(self):
        updated_first_name = self.first_name_entry.get()
        updated_last_name = self.last_name_entry.get()
        updated_phone = self.phone_no_entry.get()
        updated_username = self.username_entry.get()
        updated_password = self.password_entry.get()

        update_details = """
                                UPDATE users_info
                                SET first_name = %s, second_name = %s, phone_no = %s, username = %s, password = %s
                                WHERE id = %s
                         """
        self.mycursor.execute(update_details, (updated_first_name, updated_last_name, updated_phone, updated_username,
                                               updated_password, self.user_id))
        self.mydb.commit()

    def check_otp(self):
        if self.enter_otp_entry.get() == str(self.otp):
            self.if_otp_true = True
            self.view_profile_scr.destroy()
            self.view_profile()
        else:
            self.if_otp_true = False
            wrong_otp_label = Label(self.get_otp_frame, text = "Wrong OTP", fg = 'red', font = (None, 15))
            wrong_otp_label.place(x = 30, y = 100)

    def get_coupon(self, scr):
        self.coupon_code = None
        max_coupons = self.points // 200
        if max_coupons > 0:
            self.coupon_code = ''
            key = "ACHCEWardressNCUERNV93841237482323"

            for i in range(10):
                random_num = random.randint(0, len(key) - 1)
                self.coupon_code += key[random_num]

            coupon_label = Label(scr, text = "Your Coupon code is : ", font = (None, 13),
                                 fg = 'green', padx = 20)
            coupon_label.place(x = 930, y = 150)

            coupon_no = Entry(scr, font = (None, 13), fg = 'green')
            coupon_no.insert(0, self.coupon_code)
            coupon_no.place(x = 1150, y = 150)
        else:
            max_coupon_label = Label(scr,
                                     text = "You need 200 points to avail coupon\n you currently have {} points".
                                     format(self.points), font = (None, 13), fg = "red")
            max_coupon_label.place(x = 930, y = 150)
            max_coupon_label.after(10000, lambda: max_coupon_label.destroy())

        self.get_coupon_button.configure(state=DISABLED)

    def view_points(self):
        view_points_scr = Toplevel(self.account_detail_scr)
        view_points_scr.wm_state('zoomed')
        view_points_scr.title("View Points")

        logo_image = ImageTk.PhotoImage(self.logo_image)
        logo_label = Label(view_points_scr, image = logo_image)
        logo_label.image = logo_image
        logo_label.place(x = 0, y = 0)

        get_points = "SELECT points FROM users_info WHERE id = %s"
        self.mycursor.execute(get_points, (self.user_id, ))

        point_stage2 = self.mycursor.fetchall()
        point_stage1 = point_stage2[0]
        if point_stage1[0] is None:
            self.points = 0
        else:
            self.points = point_stage1[0]
        display_points_label = Label(view_points_scr, text = "Your Current points are:- {}".format(self.points),
                                     font = (None, 35))
        display_points_label.place(x = 100, y = 170)

        point_info_frame = Frame(view_points_scr, width = 1250, height = 150, bd = 3, relief = RIDGE)
        point_info_frame.place(x = 80, y = 420)

        points_info = "Points are special offers provided by The Ganges it is a quick and convenient way " \
                      "to save money. \n" \
                      "On every order placed You receive 10 points, " \
                      "which can be redeemed in future to avail shopping vouchers, prizes and etc." \
                      "Every 200 points account for a voucher worth ₹ 150.\nOn reaching the " \
                      "milestone of 1000 points you have a chance to win a Ganges original Smart TV " \
                      "There is no minimum order to redeem the voucher.\n\nTo use your collected points" \
                      "you need to first convert them to a free one-time voucher and then redeem it " \
                      "at the time of checkout. Please note that you can NOT pay the full order using " \
                      "points at least 10% of the order must be paid with other means like Credit card," \
                      "Debit card, Cash On Delivery or Net Banking!"

        points_info_label = Message(point_info_frame, text = points_info, width = 1200, font = (None, 13))
        points_info_label.place(x = 0, y = 0)

        self.get_coupon_button = Button(view_points_scr, text = "Get Coupon", bg = 'DarkOrange1', padx = 10,
                                        pady = 5, activebackground = 'DarkOrange1', font = (None, 15),
                                        command = lambda: self.get_coupon(view_points_scr))
        self.get_coupon_button.place(x = 1000, y = 170)

    def order_frame_binder(self, event):
        self.order_scr_canvas.configure(scrollregion = self.main_scr_canvas.bbox("all"), width = 1340, height = 590)
        return event

    def scroll_order_frame(self, event):
        self.order_scr_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def view_orders(self):
        view_order_scr = Toplevel(self.account_detail_scr)
        view_order_scr.wm_state('zoomed')
        view_order_scr.title('Track Order')

        logo_image = ImageTk.PhotoImage(self.logo_image)
        logo_label = Label(view_order_scr, image = logo_image)
        logo_label.image = logo_image
        logo_label.place(x = 0, y = 0)

        order_outer_frame = Frame(view_order_scr)
        order_outer_frame.place(x = 1, y = 100)

        self.order_scr_canvas = Canvas(order_outer_frame)
        order_scr_frame = Frame(self.order_scr_canvas)
        order_scr_frame.pack()
        order_scrollbar = Scrollbar(order_outer_frame, orient = "vertical", command = self.order_scr_canvas.yview)
        self.order_scr_canvas.configure(yscrollcommand = order_scrollbar.set)

        order_scrollbar.pack(side = "right", fill = "y")
        self.order_scr_canvas.pack()
        self.order_scr_canvas.create_window((0, 0), window = order_scr_frame)

        order_scr_frame.bind("<Configure>", self.order_frame_binder)
        self.order_scr_canvas.bind_all("<MouseWheel>", self.scroll_order_frame)

        view_orders = "SELECT product_id, quantity, current_status FROM transaction_status " \
                      "WHERE current_status != 'C' AND user_id = %s;"
        self.mycursor.execute(view_orders, (self.user_id, ))
        all_orders = self.mycursor.fetchall()

        if len(all_orders) == 0:
            no_order_label = Label(order_scr_frame, text = "No Orders Placed", font = (None, 40), fg ='red')
            no_order_label.grid(row = 1, column = 1)

            go_to_cart_button = Button(order_scr_frame, text = "View Cart", font = (None, 25), bg = 'DarkOrange',
                                       command = self.view_cart)
            go_to_cart_button.grid(row = 2, column = 1)
        else:
            row_coord = 0
            for orders in all_orders:
                product_id = orders[0]
                product_quantity = orders[1]
                current_status = orders[2]

                self.status = current_status

                get_product_info = "SELECT product_name, image_path, price FROM products_info WHERE id = %s"
                self.mycursor.execute(get_product_info, (product_id, ))
                product_info_stage2 = self.mycursor.fetchall()
                product_info = product_info_stage2[0]

                product_name = product_info[0]
                product_image_url = product_info[1]
                product_price = product_info[2]

                display_orders_frame = Frame(order_scr_frame, height = 200, width = 1300, bd = 10, relief = SUNKEN)
                display_orders_frame.grid(row = row_coord, column = 0)

                product_image = Image.open(product_image_url)
                product_image = product_image.resize((150, 150))
                product_ren = ImageTk.PhotoImage(product_image)

                product_image_label = Label(display_orders_frame, image = product_ren)
                product_image_label.image = product_ren
                product_image_label.place(x = 0, y = 15)

                product_name_label = Label(display_orders_frame, text = product_name, font = (None, 15))
                product_name_label.place(x = 180, y = 50)

                product_quantity_label = Label(display_orders_frame, text = "Quantity : {}".format(product_quantity),
                                               font = (None, 15))
                product_quantity_label.place(x = 180, y = 100)

                locale.setlocale(locale.LC_ALL, 'en_US')
                formatted_price = locale.format_string("%d", int(product_price), grouping = True)

                product_price_label = Label(display_orders_frame, text = "price : ₹ " + formatted_price,
                                            font = (None, 15))
                product_price_label.place(x = 180, y = 130)

                product_amount = product_quantity * product_price
                product_amount_label = Label(display_orders_frame, text = "Amount : " + str(product_amount),
                                             font = (None, 15))
                product_amount_label.place(x = 600, y = 50)

                current_status_label = Label(display_orders_frame, text = "Product Status: " + current_status,
                                             font = (None, 15))
                current_status_label.place(x = 600, y = 100)

                row_coord += 1

    def account_details(self):
        self.account_detail_scr = Toplevel(self.win)
        self.account_detail_scr.wm_state('zoomed')
        self.account_detail_scr.title('Account Details')

        logo_image = ImageTk.PhotoImage(self.logo_image)
        logo_label = Label(self.account_detail_scr, image = logo_image)
        logo_label.image = logo_image
        logo_label.place(x = 0, y = 0)

        self.view_cart_button = Button(self.account_detail_scr, text = "View Cart items", relief = RIDGE, bg = 'white',
                                       font = (None, 20), padx = 20, pady = 20, command = self.view_cart)
        self.view_cart_button.place(x = 100, y = 200)

        self.view_profile_button = Button(self.account_detail_scr, text = "View Profile Details", relief = RIDGE,
                                          bg = 'white', font = (None, 20), padx = 10, pady = 20,
                                          command = self.view_profile)
        self.view_profile_button.place(x = 400, y = 200)

        self.view_points_button = Button(self.account_detail_scr, text = "View Points", relief = RIDGE, bg = 'white',
                                         font = (None, 20), padx = 40, pady = 20, command = self.view_points)
        self.view_points_button.place(x = 700, y = 200)

        self.view_order_button = Button(self.account_detail_scr, text = "Track Orders", relief = RIDGE, bg = 'white',
                                        font = (None, 20), padx = 40, pady = 20, command = self.view_orders)
        self.view_order_button.place(x = 1000, y = 200)

        sign_out_image = Image.open("sign_out.jpg")
        sign_out_image = sign_out_image.resize((100, 100))
        sign_out_render = ImageTk.PhotoImage(sign_out_image)

        sign_out_button = Button(self.account_detail_scr, image = sign_out_render, bd = 0,
                                 command = lambda: self.log_out(self.account_detail_scr))
        sign_out_button.image = sign_out_render
        sign_out_button.place(x = 1100, y = 0)

    def backspace_pressed(self, event):
        delete_name = self.search_entry.get()
        if len(delete_name) == len(self.search_name):
            widget_list = self.get_all_widgets()
            for item in widget_list:
                item.destroy()
            self.place_products()
        return event

    def inner_frame_binder(self, event):
        self.main_scr_canvas.configure(scrollregion = self.main_scr_canvas.bbox("all"), width = 1340, height = 590)
        return event

    def get_all_widgets(self):
        widget_list = self.main_scr_frame.winfo_children()

        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())

        return widget_list

    def search_item(self):
        try:
            self.search_name = self.search_entry.get()
            code6 = "SELECT image_path, id FROM products_info WHERE product_name = %s; "
            self.mycursor.execute(code6, (self.search_name,))
            info_stage2 = self.mycursor.fetchall()
            info_stage1 = info_stage2[0]

            widget_list = self.get_all_widgets()

            for item in widget_list:
                item.destroy()

            but_image = Image.open(info_stage1[0])
            product_image_size = (194, 193)
            but_image = but_image.resize(product_image_size)

            but_render = ImageTk.PhotoImage(but_image)

            self.but_button = Button(self.main_scr_frame, image = but_render, bd = 12)
            self.but_button.config(command = partial(self.product_info, info_stage1[1]))

            self.but_button.image = but_render
            self.but_button.place(x = 0, y = 0)

        except IndexError:
            pass

    def scroll_canvas(self, event):
        self.main_scr_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def place_products(self):
        get_image_details = "SELECT image_path FROM products_info"
        self.mycursor.execute(get_image_details)
        image_details_2d_array = self.mycursor.fetchall()

        row = 0
        column = 0

        self.current_id = 1
        product_image_size = (194, 193)

        for image_path_stage2 in image_details_2d_array:
            image_path = image_path_stage2[0]

            product_image = Image.open(image_path)
            product_image = product_image.resize(product_image_size)
            product_image_render = ImageTk.PhotoImage(product_image)

            product_buttons = Button(self.main_scr_frame, image = product_image_render, bd = 12)
            product_buttons.config(command = partial(self.product_info, self.current_id))
            product_buttons.image = product_image_render
            product_buttons.grid(row = row, column = column)

            column += 1
            self.current_id += 1

            if column == 6:
                column = 0
                row += 1

    def product_info(self, product_id):
        self.product_id = product_id
        product_info_screen = Toplevel(self.win)
        product_info_screen.wm_state('zoomed')
        product_info_screen.title('Product Info')

        get_details_from_id = "SELECT * FROM products_info WHERE id = %s"
        self.mycursor.execute(get_details_from_id, (product_id,))

        product_details_2d = self.mycursor.fetchall()
        product_details = product_details_2d[0]

        product_image_address = product_details[2]
        product_name = product_details[0]
        product_information = product_details[4]
        product_price = product_details[3]
        product_stock = product_details[1]

        self.main_product_frame = LabelFrame(product_info_screen, text = str(product_name), width = 1000, height = 675)
        self.main_product_frame.configure(font = ("Nevrada", 27))
        self.main_product_frame.place(x = 10, y = 0)

        image_reference_size = (300, 300)
        image_reference = Image.open(product_image_address)
        image_reference = image_reference.resize(image_reference_size)
        image_reference_render = ImageTk.PhotoImage(image_reference)

        image_reference_label = Label(self.main_product_frame, image = image_reference_render)
        image_reference_label.image = image_reference_render
        image_reference_label.place(x = 40, y = 70)

        product_name_label = Label(self.main_product_frame, text = "Product Name: " + product_name,
                                   font = ('Nevrada', 20))
        product_name_label.place(x = 450, y = 150)

        locale.setlocale(locale.LC_ALL, 'en_US')
        formatted_price = locale.format_string("%d", int(product_price), grouping = True)

        product_price_label = Label(self.main_product_frame, text = "Price: ₹" + formatted_price,
                                    font = ('Nevrada', 20))
        product_price_label.place(x = 450, y = 200)

        product_information_label_heading = Label(self.main_product_frame, text = "Product Details", fg = 'FireBrick1')
        product_information_label_heading.configure(font = ('Genuine', 13, 'bold'))
        product_information_label_heading.place(x = 60, y = 410)

        product_information_label = Message(self.main_product_frame, text = product_information, width = 900)
        product_information_label.place(x = 60, y = 440)

        in_stock_label = "Will be defined in if statement"
        fg_stock = "Will be defined in if statement"
        if product_stock > 10:
            in_stock_label = "In Stock"
            fg_stock = "lime green"
        elif 0 < product_stock <= 10:
            in_stock_label = "Hurry! Only " + product_stock + " items left"
            fg_stock = "brown4"
        elif product_stock == 0:
            in_stock_label = "None Left!"
            fg_stock = 'red4'

        product_stock_label = Label(self.main_product_frame, text = in_stock_label, fg = fg_stock,
                                    font = ('Nevrada', 15))
        product_stock_label.place(x = 450, y = 250)

        quantity_heading_label = Label(self.main_product_frame, text = 'Quantity: ', font = ('Nevrada', 17))
        quantity_heading_label.place(x = 450, y = 280)

        quantity_lists = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, '10+'
        ]
        self.option_variable.set(quantity_lists[0])

        self.quantity_option_menu = OptionMenu(self.main_product_frame, self.option_variable, *quantity_lists,
                                               command = self.get_quantity)
        self.quantity_option_menu['menu'].config(font = ('Arial', 10))
        self.quantity_option_menu.config(width = 3, font = ('Arial', 10))
        self.quantity_option_menu.place(x = 560, y = 280)

        add_to_cart_img_size = (300, 113)
        add_to_cart_img = Image.open('cart.png')
        add_to_cart_img = add_to_cart_img.resize(add_to_cart_img_size)
        add_to_cart_ren = ImageTk.PhotoImage(add_to_cart_img)

        add_to_cart_button = Button(product_info_screen, image = add_to_cart_ren, bd = 0)
        add_to_cart_button.config(command = self.add_to_cart)
        add_to_cart_button.image = add_to_cart_ren
        add_to_cart_button.place(x = 900, y = 300)

    def get_quantity(self, quantity):
        if quantity == '10+':
            self.quantity_option_menu.destroy()
            self.quantity_entry = Entry(self.main_product_frame, font = ('arial', 12), width = 10)
            self.quantity_entry.place(x = 550, y = 287)

    def login_register(self, command, button_clicked):
        if command == 'login':

            username = self.username_entry.get()
            password = self.password_entry.get()

            get_users = "SELECT username FROM users_info"
            self.mycursor.execute(get_users)
            username_list_stage2 = self.mycursor.fetchall()
            username_list = []
            for user in username_list_stage2:
                username_list.append(user[0])

            if username in username_list:
                get_passwords = "SELECT password, id FROM users_info WHERE username = %s"
                self.mycursor.execute(get_passwords, (username,))
                password_list_stage2 = self.mycursor.fetchall()
                password_list = password_list_stage2[0]
                self.user_id = password_list[1]
                real_password = password_list[0]
                if password == real_password:

                    self.if_logged_in = True
                    if self.stay_signed:
                        make_user_stay_signed = """
                                               UPDATE users_info
                                               SET if_signed_in = TRUE
                                               WHERE id = %s
                                           """
                        self.mycursor.execute(make_user_stay_signed, (self.user_id,))
                        self.mydb.commit()

                        make_other_users = """
                                                UPDATE users_info
                                                SET if_signed_in = FALSE
                                                WHERE id != %s
                        
                                            """
                        self.mycursor.execute(make_other_users, (self.user_id,))
                        self.mydb.commit()
                    self.view_account_button.destroy()
                    self.win.after(0, self.main_menu)

                    if button_clicked == "add":
                        self.add_to_cart()
                    elif button_clicked == "view_account":
                        self.account_details()
                    else:
                        self.view_cart()

                    self.username_entry.delete(0, END)
                    self.password_entry.delete(0, END)

                else:
                    password_not_found_label = Label(self.login_frame, text = "Wrong Password", fg = 'red')
                    password_not_found_label.configure(bg = 'white', font = (None, 12))
                    password_not_found_label.place(x = 80, y = 260)
                    self.password_entry.delete(0, END)
                    password_not_found_label.after(10000, lambda: password_not_found_label.destroy())
            else:
                username_not_found_label = Label(self.login_frame, text = "Username not found", fg = 'red')
                username_not_found_label.configure(bg = 'white', font = (None, 12))
                username_not_found_label.place(x = 80, y = 110)
                self.password_entry.delete(0, END)
                username_not_found_label.after(10000, lambda: username_not_found_label.destroy())
        elif command == 'register':
            register_scr = Toplevel(self.win)
            register_scr.wm_state('zoomed')
            register_scr.title('Register')
            register_scr.configure(bg = 'ghost white')

            self.register_frame = Frame(register_scr, bd = 12, relief = RIDGE, height = 700, width = 500, bg = 'azure')
            self.register_frame.place(x = 400, y = 0)

            entry_name_label = Label(self.register_frame, text = 'Enter First Name:-', font = ('Arial', 19),
                                     bg = 'azure')
            entry_name_label.place(x = 0, y = 0)
            self.entry_name = Entry(self.register_frame, font = ('Arial', 17))
            self.entry_name.place(x = 100, y = 35)

            last_name_label = Label(self.register_frame, text = "Enter Last Name:-", font = ('Arial', 19), bg = 'azure')
            last_name_label.place(x = 0, y = 90)
            self.last_name_entry = Entry(self.register_frame, font = ('Arial', 17))
            self.last_name_entry.place(x = 100, y = 125)

            phone_no_label = Label(self.register_frame, text = "Enter Phone Number:-", font = ('Arial', 19),
                                   bg = 'azure')
            phone_no_label.place(x = 0, y = 185)
            self.phone_no_entry = Entry(self.register_frame, font = ('Arial', 17))
            self.phone_no_entry.place(x = 100, y = 220)

            username_label = Label(self.register_frame, text = "Enter a Username:-", font = ('Arial', 19), bg = 'azure')
            username_label.place(x = 0, y = 280)
            self.new_username_entry = Entry(self.register_frame, font = ('Arial', 17))
            self.new_username_entry.place(x = 100, y = 315)

            new_password_label = Label(self.register_frame, text = "Enter Password:-", font = ('Arial', 19),
                                       bg = 'azure')
            new_password_label.place(x = 0, y = 375)
            self.new_password_entry = Entry(self.register_frame, font = ("Arial", 17), show = "●")
            self.new_password_entry.place(x = 100, y = 410)

            create_account_button = Button(self.register_frame, text = "Create New Account", pady = 5, padx = 20)
            create_account_button.configure(bg = 'orange', font = ('Arial', 20), command = self.new_user)
            create_account_button.place(x = 75, y = 500)

            already_account_label = Label(self.register_frame, text = "Already have an Account.", bg = 'azure')
            already_account_label.place(x = 140, y = 565)
            already_account_button = Button(self.register_frame, text = 'Sign In', fg = 'blue', bd = 0)
            already_account_button.configure(bg = 'azure',
                                             command = lambda: (self.add_to_cart(), register_scr.destroy()))
            already_account_button.place(x = 280, y = 565)

    def new_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        new_first_name = self.entry_name.get()
        new_last_name = self.last_name_entry.get()
        new_phone = self.phone_no_entry.get()

        get_username = "SELECT username FROM  users_info;"
        self.mycursor.execute(get_username)
        list_of_username_stage2 = self.mycursor.fetchall()
        list_of_username = list_of_username_stage2[0]
        if new_username in list_of_username:
            username_exists_label = Label(self.register_frame, text = 'username already exists',
                                          fg = 'red', bg = 'azure')
            username_exists_label.place(x = 150, y = 355)
            username_exists_label.after(10000, lambda: username_exists_label.destroy())
            self.username_entry.delete(0, END)
        else:

            insert_new_user = """
                        INSERT INTO users_info(first_name, second_name, phone_no, username, password)
                        VALUES (%s,%s,%s,%s,%s)
            """

            self.mycursor.execute(insert_new_user, (str(new_first_name), str(new_last_name), int(new_phone),
                                                    str(new_username), str(new_password)))
            self.mydb.commit()

    def stay_sign_in(self):
        self.stay_signed = True

    def show_pass(self):
        password = self.password_entry.get()
        self.password_entry.delete(0, END)

        if self.pass_count % 2 == 0:
            self.password_entry.config(show = "")
            self.password_entry.insert(0, password)
        else:
            self.password_entry.config(show = "●")
            self.password_entry.insert(0, password)
        self.pass_count += 1

    def default_login(self, button_clicked):
        get_signed_in_user = "SELECT id FROM users_info WHERE if_signed_in = TRUE"
        self.mycursor.execute(get_signed_in_user)
        signed_in_user_stage2 = self.mycursor.fetchall()
        if len(signed_in_user_stage2) != 0:
            signed_in_user = signed_in_user_stage2[0]
            self.user_id = signed_in_user[0]
            self.if_logged_in = True
            self.add_to_cart()
        else:
            self.yes = "yes"
            self.add_to_cart_scr = Toplevel(self.win)
            self.add_to_cart_scr.wm_state('zoomed')

            login_warning_label = Label(self.add_to_cart_scr, text = "Login to continue!")
            login_warning_label.config(font = ('Arial', 20), bg = 'ghost white')
            login_warning_label.place(x = 520, y = 60)

            self.login_frame = Frame(self.add_to_cart_scr, bd = 12, relief = RIDGE, height = 400, width = 400,
                                     bg = 'white')
            self.login_frame.place(x = 450, y = 100)

            enter_username_label = Label(self.login_frame, text = "Enter Username :-", font = (None, 20), bg = 'white')
            enter_username_label.place(x = 0, y = 10)

            self.username_entry = Entry(self.login_frame, font = (None, 19), bd = 5)
            self.username_entry.place(x = 50, y = 60)

            enter_password_label = Label(self.login_frame, text = "Enter Password :-", font = (None, 20), bg = 'white')
            enter_password_label.place(x = 0, y = 130)

            self.password_entry = Entry(self.login_frame, font = (None, 19), bd = 5, show = "●")
            self.password_entry.place(x = 30, y = 190)

            eye_image = Image.open("show_pass.png")
            eye_image_size = (55, 25)
            eye_image = eye_image.resize(eye_image_size)
            eye_render = ImageTk.PhotoImage(eye_image)

            eye_button = Button(self.login_frame, image = eye_render, bg = 'white', bd = 0,
                                activebackground = 'white', command = self.show_pass)
            eye_button.image = eye_render
            eye_button.place(x = 320, y = 197)

            stay_signed_in = Checkbutton(self.login_frame, text = "Stay signed in", bg = 'white', font = (None, 12),
                                         command = self.stay_sign_in)
            stay_signed_in.place(x = 50, y = 250)

            login_button = Button(self.login_frame, text = "Login", font = ("Arial", 17), padx = 40, bg = 'orange',
                                  bd = 5)
            login_button.configure(activebackground = 'orange', pady = 3,
                                   command = lambda: self.login_register('login', button_clicked))
            login_button.place(x = 112, y = 300)

            sign_up_label = Label(self.add_to_cart_scr, text = "Don't have an account? Sign Up for free",
                                  font = (None, 15))
            sign_up_label.place(x = 470, y = 500)

            sign_up_button = Button(self.add_to_cart_scr, text = 'Sign Up', font = ("Arial", 17), bg = 'orange')
            sign_up_button.config(activebackground = 'orange', pady = 3, bd = 4,
                                  command = lambda: (self.login_register('register', button_clicked),
                                                     self.add_to_cart_scr.destroy()))
            sign_up_button.place(x = 600, y = 550)

    def add_to_cart(self):
        if self.if_logged_in:
            add_to_cart_scr = Toplevel(self.win)
            add_to_cart_scr.wm_state('zoomed')
            if self.option_variable.get() == '10+':
                quantity = self.quantity_entry.get()
            else:
                quantity = self.option_variable.get()
            current_datetime = datetime.now()
            dt_string = current_datetime.strftime("%Y/%m/%d %H:%M:%S")

            already_items = "SELECT product_id, quantity FROM transaction_status WHERE product_id = %s" \
                            " and current_status = 'C' and user_id = %s"
            self.mycursor.execute(already_items, (self.product_id, self.user_id))

            same_item_stage2 = self.mycursor.fetchall()
            if len(same_item_stage2) != 0:
                for same_item_stage1 in same_item_stage2:
                    quantity = int(quantity)
                    quantity += same_item_stage1[1]

                    delete_same_item = "DELETE FROM transaction_status WHERE user_id = %s AND product_id = %s AND" \
                                       " current_status = 'C'"
                    self.mycursor.execute(delete_same_item, (self.user_id, self.product_id))

            add_to_cart_info = "SELECT * FROM products_info WHERE id = %s;"
            self.mycursor.execute(add_to_cart_info, (self.product_id,))
            add_info_stage2 = self.mycursor.fetchall()
            add_info_stage1 = add_info_stage2[0]

            image_url = add_info_stage1[2]
            product_name = add_info_stage1[0]

            product_image = Image.open(image_url)
            product_image_size = (100, 100)
            product_image = product_image.resize(product_image_size)
            product_render = ImageTk.PhotoImage(product_image)

            add_to_cart_frame = Frame(add_to_cart_scr, bd = 12, height = 700, width = 1355, relief = RIDGE)
            add_to_cart_frame.place(x = 0, y = 0)

            product_image_label = Label(add_to_cart_frame, image = product_render, bd = 10, relief = RIDGE)
            product_image_label.image = product_render
            product_image_label.place(x = 100, y = 100)

            get_stocks = "SELECT product_stocks FROM products_info WHERE id = %s"
            self.mycursor.execute(get_stocks, (self.product_id,))
            stock_stage2 = self.mycursor.fetchall()
            stock_stage1 = stock_stage2[0]
            scr_title = "Add item to cart"

            if int(quantity) < int(stock_stage1[0]):
                insert_items = """
                                           INSERT INTO transaction_status(user_id, product_id, quantity, current_status, datetime)
                                           VALUES (%s, %s, %s, %s, %s)

                           """
                self.mycursor.execute(insert_items, (self.user_id, self.product_id, quantity, "C", dt_string))
                self.mydb.commit()

                product_name_label = Label(add_to_cart_frame, text = product_name + " added to cart",
                                           font = ('Arial', 20), fg = 'lime green')
                product_name_label.place(x = 220, y = 140)

                total_cart_items = "SELECT SUM(quantity) FROM transaction_status WHERE user_id = %s and current_status = %s;"
                self.mycursor.execute(total_cart_items, (self.user_id, "C"))
                cart_items_list = self.mycursor.fetchall()
                cart_items = cart_items_list[0]
                quantity = cart_items[0]

                if cart_items[0] is None:
                    quantity = 0

                cart_subtotal_label = Label(add_to_cart_frame, text = "Cart Subtotal:- (" + str(quantity) + " items)",
                                            font = ('None', 20))
                cart_subtotal_label.place(x = 600, y = 140)

            else:
                product_name_label = Label(add_to_cart_frame, text = product_name + " not added to cart",
                                           font = ('Arial', 20), fg = 'red')
                product_name_label.place(x = 220, y = 140)

        else:
            scr_title = "Log In or Sign Up"
            self.default_login("add")
        if self.yes == "yes":
            self.add_to_cart_scr.title(scr_title)

    def scroll_view_canvas(self, event):
        try:
            self.view_cart_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        except TclError:
            pass

    def view_frame_binder(self, event):
        self.view_cart_canvas.configure(scrollregion = self.view_cart_canvas.bbox("all"), width = 1340, height = 490)
        return event

    def remove_item(self, product_id, scr, command):
        remove_item = "DELETE FROM transaction_status WHERE user_id = %s AND product_id = %s and current_status = %s"
        self.mycursor.execute(remove_item, (self.user_id, product_id, self.status))
        self.mydb.commit()

        a = str(scr).find('.!toplevel')
        if a != -1:
            scr.destroy()
        if command == "view_cart":
            self.win.after(0, self.view_cart)
        elif command == "view_order":
            self.win.after(0, self.view_orders)

    def order_finished_screen(self, total, disc):
        get_quantity = "SELECT quantity FROM transaction_status WHERE user_id = %s AND current_status = 'C';"
        self.mycursor.execute(get_quantity, (self.user_id,))
        quantities = self.mycursor.fetchall()

        pre_quantity = 0

        for quantity in quantities:
            pre_quantity += quantity[0]
        self.points = pre_quantity * 10

        get_items = "SELECT product_id FROM transaction_status WHERE user_id = %s AND current_status = 'C';"
        self.mycursor.execute(get_items, (self.user_id,))

        all_items_stage2 = self.mycursor.fetchall()

        for items in all_items_stage2:
            change_item_state = """
                                           UPDATE transaction_status
                                           SET current_status = 'DELIVERED'
                                           WHERE user_id = %s AND product_id = %s
                   """
            self.mycursor.execute(change_item_state, (self.user_id, items[0]))
            self.mydb.commit()

        order_placed_scr = Toplevel(self.checkout_scr)
        order_placed_scr.wm_state('zoomed')
        order_placed_scr.title('Order Placed')

        order_placed_label = Label(order_placed_scr, text = "Your order will be arriving soon",
                                   font = (None, 40))
        self.notify.send(str(total))
        order_placed_label.place(x = 200, y = 300)
        if disc:
            self.points -= 200
            update_points = "UPDATE users_info SET points = %s WHERE id = %s"
            self.mycursor.execute(update_points, (self.points, self.user_id))
            self.mydb.commit()
        else:
            update_points = "UPDATE users_info SET points = %s WHERE id = %s"
            self.mycursor.execute(update_points, (self.points, self.user_id))
            self.mydb.commit()

    def order_place(self):
        order_preview_screen = Toplevel(self.checkout_frame)
        order_preview_screen.wm_state('zoomed')
        order_preview_screen.title('Order Preview')

        logo_size = (400, 100)
        logo_image = self.logo_image.resize(logo_size)
        logo_render = ImageTk.PhotoImage(logo_image)

        logo_label = Label(order_preview_screen, image = logo_render)
        logo_label.image = logo_render
        logo_label.place(x = 0, y = 0)

        order_subtotal_frame = LabelFrame(order_preview_screen, text = 'Order Subtotal Frame', font = (None, 13),
                                          bd = 2, relief = RIDGE, width = 600, height = 300)
        order_subtotal_frame.place(x = 10, y = 200)

        subtotal_label = Label(order_subtotal_frame, text = 'Subtotal :\t₹ {}'.format(self.subtotal), font = (None, 11),
                               fg = 'honeydew4')
        subtotal_label.place(x = 0, y = 5)

        tax = self.subtotal * 0.02
        tax_label = Label(order_subtotal_frame, text = 'GST :\t₹ {}'.format(tax), font = (None, 11), fg = 'honeydew4')
        tax_label.place(x = 0, y = 30)
        if self.discount_eligible:

            discount_label = Label(order_subtotal_frame, text = "Discount:   ₹{}".format(-150), font = (None, 11),
                                   fg = 'honeydew4')
            discount_label.place(x = 0, y = 50)
            total = self.subtotal + tax - 150
            disc = True
        else:
            total = self.subtotal + tax
            discount_label = Label(order_subtotal_frame, text = "Discount:   ₹{}".format(0), font = (None, 11),
                                   fg = 'honeydew4')
            discount_label.place(x = 0, y = 50)
            disc = False

        total_label = Label(order_subtotal_frame, text = 'Total :\t₹{}'.format(total), font = (None, 11),
                            fg = 'honeydew4')
        total_label.place(x = 0, y = 100)

        confirm_order_button = Button(order_subtotal_frame, text = "Confirm Order", font = (None, 11), bg = 'DarkOrange',
                                      command = lambda: self.order_finished_screen(total, disc))
        confirm_order_button.place(x = 100, y = 200)

        self.discount_eligible = False

    def place_order(self, payment_mode):
        if payment_mode == 'net banking':
            self.bank_name = self.radio_var.get()
            if self.bank_name == "hdfc":
                webbrowser.open("https://netbanking.hdfcbank.com/netbanking/")
                self.notify.send("Your HDFC account was debited with ₹" + self.subtotal_str)
                self.order_place()
            elif self.bank_name == "icici":
                webbrowser.open("https://www.icicibank.com/Personal-Banking/insta-banking/internet-banking/index.page")
                self.notify.send("Your ICICI account was debited with ₹" + self.subtotal_str)
                self.order_place()
            elif self.bank_name == "axis":
                webbrowser.open("https://www.axisbank.com/bank-smart/internet-banking/getting-started")
                self.notify.send("Your Axis account was debited with ₹" + self.subtotal_str)
                self.order_place()
            elif self.bank_name == "kotak":
                webbrowser.open("https://www.kotak.com/en/digital-banking/ways-to-bank/net-banking.html")
                self.notify.send("Your Kotak Mahindra account was debited with ₹" + self.subtotal_str)
                self.order_place()
            elif len(self.bank_name) == 0:
                messagebox.showerror('error', 'select a bank name')
        else:
            self.order_place()

    def payment_option(self, option):
        self.payment_mode = option
        place_order_button = Button(self.checkout_frame, text = "Place Order", font = (None, 25))

        if option == "Net Banking":
            net_frame = Frame(self.checkout_scr, width = 400, height = 500, bd = 12, relief = RIDGE)
            net_frame.place(x = 950, y = 120)

            bank_name_label = Label(net_frame, text = "Select a bank name", font = (None, 30))
            bank_name_label.place(x = 0, y = 0)

            hdfc_bank_rb = Radiobutton(net_frame, text = "HDFC bank", variable = self.radio_var,
                                       value = "hdfc", font = (None, 15),)
            hdfc_bank_rb.place(x = 30, y = 70)

            icici_bank_rb = Radiobutton(net_frame, text = "ICICI bank", variable = self.radio_var,
                                        value = "icici", font = (None, 15),)
            icici_bank_rb.place(x = 30, y = 120)

            axis_bank_rb = Radiobutton(net_frame, text = "Axis bank", variable = self.radio_var,
                                       value = "axis", font = (None, 15),)
            axis_bank_rb.place(x = 30, y = 170)

            kotak_bank_rb = Radiobutton(net_frame, text = "Kotak Mahindra bank", variable = self.radio_var,
                                        value = "kotak", font = (None, 15),)
            kotak_bank_rb.place(x = 30, y = 220)

            place_order_button.config(command = lambda: self.place_order("net banking"))
            place_order_button.place(x = 200, y = 400)

        elif option == "Credit Card":
            credit_frame = Frame(self.checkout_scr, width = 400, height = 500, bd = 12, relief = RIDGE)
            credit_frame.place(x = 950, y = 120)

            enter_credit_label = Label(credit_frame, text = "Enter Credit card details", font = (None, 25))
            enter_credit_label.place(x = 0, y = 0)

            cvv_label = Label(credit_frame, text = "Enter CVV", font = (None, 15))
            cvv_label.place(x = 30, y = 70)

            cvv_entry = Entry(credit_frame, font = (None, 13))
            cvv_entry.place(x = 30, y = 120)

            expiry_year_label = Label(credit_frame, text = 'Expiry Date:', font = (None, 17))
            expiry_year_label.place(x = 30, y = 170)
            expiry_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
            self.expiry_var.set(expiry_years[0])

            expiry_year_menu = OptionMenu(credit_frame, self.expiry_var, *expiry_years)
            expiry_year_menu.configure(width = 8)
            expiry_year_menu.place(x = 180, y = 170)

            place_order_button.config(command = lambda: self.place_order("credit"))
            place_order_button.place(x = 200, y = 400)

        elif option == "Debit Card":
            debit_frame = Frame(self.checkout_scr, width = 400, height = 500, bd = 12, relief = RIDGE)
            debit_frame.place(x = 950, y = 120)

            enter_debit_label = Label(debit_frame, text = "Enter Debit card details", font = (None, 25))
            enter_debit_label.place(x = 0, y = 0)

            cvv_label = Label(debit_frame, text = "Enter CVV", font = (None, 15))
            cvv_label.place(x = 30, y = 70)

            cvv_entry = Entry(debit_frame, font = (None, 13))
            cvv_entry.place(x = 30, y = 120)

            expiry_year_label = Label(debit_frame, text = 'Expiry Date:', font = (None, 17))
            expiry_year_label.place(x = 30, y = 170)
            expiry_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
            self.expiry_var.set(expiry_years[0])

            expiry_year_menu = OptionMenu(debit_frame, self.expiry_var, *expiry_years)
            expiry_year_menu.configure(width = 8)
            expiry_year_menu.place(x = 180, y = 170)

            place_order_button.config(command = lambda: self.place_order("debit"))
            place_order_button.place(x = 200, y = 400)

        elif option == "Cash On Delivery (COD)":
            cod_frame = Frame(self.checkout_scr, width = 400, height = 500, bd = 12, relief = RIDGE)
            cod_frame.place(x = 950, y = 120)

            cod_money = Label(cod_frame, text = "Cash on Delivery", font = (None, 27))
            cod_money.place(x = 50, y = 200)

            place_order_button.config(command = lambda: self.place_order("cod"))
            place_order_button.place(x = 200, y = 400)

    def checkout(self):
        self.checkout_scr = Toplevel(self.view_cart_scr)
        self.checkout_scr.wm_state('zoomed')
        self.checkout_scr.title("Checkout")

        logo_size = (400, 100)
        logo_image = self.logo_image.resize(logo_size)
        logo_render = ImageTk.PhotoImage(logo_image)

        logo_label = Label(self.checkout_scr, image = logo_render)
        logo_label.image = logo_render
        logo_label.place(x = 0, y = 0)

        self.checkout_frame = Frame(self.checkout_scr, width = 800, height = 500, bd = 12, relief = RIDGE)
        self.checkout_frame.place(x = 100, y = 120)

        address_label = Label(self.checkout_frame, text = "Enter Address: ", font = (None, 25))
        address_label.place(x = 0, y = 10)

        address_entry = Entry(self.checkout_frame, font = (None, 17))
        address_entry.place(x = 250, y = 20)

        payment_mode_var = StringVar()
        payment_option_list = ["Cash On Delivery (COD)", "Net Banking", "Credit Card", "Debit Card"]

        payment_mode_var.set("Payment Mode")
        payment_mode = OptionMenu(self.checkout_frame, payment_mode_var, *payment_option_list,
                                  command = self.payment_option)
        payment_mode.configure(font = (None, 13))
        payment_mode.place(x = 300, y = 100)

        payment_label = Label(self.checkout_frame, text = "Select Payment Mode :  ", font = (None, 20))
        payment_label.place(x = 0, y = 100)

        enter_coupon_label = Label(self.checkout_frame, text='Redeem coupon here: ', font = (None, 20))
        enter_coupon_label.place(x = 0, y = 200)

        enter_coupon_entry = Entry(self.checkout_frame, font=(None, 15))
        enter_coupon_entry.place(x = 300, y = 200)

        redeem_coupon_button = Button(self.checkout_frame, text = "Redeem Coupon", font = (None, 12),
                                      command = lambda: self.check_coupon(enter_coupon_entry))
        redeem_coupon_button.place(x = 10, y = 250)

    def check_coupon(self, entry):
        user_coupon_input = entry.get()
        if user_coupon_input == self.coupon_code:
            if self.subtotal > 200:
                discount_successful_label = Label(self.checkout_frame, text = "Discount of ₹150", font=(None, 13),
                                                  fg = 'green')
                discount_successful_label.place(x = 600, y = 200)

                self.discount_eligible = True
            else:
                minimum_discount_order_label = Message(self.checkout_frame, text = "Minimum order of ₹200 to avail the "
                                                                                   "coupon", width = 200, fg = 'red')
                minimum_discount_order_label.place(x = 500, y = 200)
                self.discount_eligible = False
        else:
            invalid_coupon_label = Label(self.checkout_frame, text = "Invalid Coupon", font = (None, 12),
                                         fg = 'Red')
            invalid_coupon_label.place(x = 600, y = 200)
            invalid_coupon_label.after(10000, lambda: invalid_coupon_label.destroy())
            self.discount_eligible = False

    def view_cart(self):
        if self.if_logged_in:
            self.subtotal = 0
            self.status = 'C'
            self.view_cart_scr = Toplevel(self.win)
            self.view_cart_scr.wm_state('zoomed')
            self.view_cart_scr.title('View Cart')

            logo_size = (400, 100)
            logo_image = self.logo_image.resize(logo_size)
            logo_render = ImageTk.PhotoImage(logo_image)

            logo_label = Label(self.view_cart_scr, image = logo_render)
            logo_label.image = logo_render
            logo_label.place(x = 0, y = 10)

            checkout_image = Image.open("checkout.PNG")
            checkout_image = checkout_image.resize((250, 40))
            checkout_render = ImageTk.PhotoImage(checkout_image)

            checkout_button = Button(self.view_cart_scr, image = checkout_render, bd = 0, command = self.checkout)
            checkout_button.image = checkout_render
            checkout_button.place(x = 1100, y = 45)

            get_in_cart_items = "SELECT product_id, quantity FROM transaction_status \
                                WHERE user_id = %s and current_status = 'C'; "
            self.mycursor.execute(get_in_cart_items, (self.user_id,))
            cart_items = self.mycursor.fetchall()
            outer_frame = Frame(self.view_cart_scr)
            outer_frame.place(x = 0, y = 150)

            self.view_cart_canvas = Canvas(outer_frame)
            view_cart_frame = Frame(self.view_cart_canvas)
            view_cart_frame.pack()
            view_scrollbar = Scrollbar(outer_frame, orient = "vertical",
                                       command = self.main_scr_canvas.yview)
            self.view_cart_canvas.configure(yscrollcommand = view_scrollbar.set)

            view_scrollbar.pack(side = "right", fill = "y")
            self.view_cart_canvas.pack()
            self.view_cart_canvas.create_window((0, 0), window = view_cart_frame)

            view_cart_frame.bind("<Configure>", self.view_frame_binder)
            self.view_cart_canvas.bind_all("<MouseWheel>", self.scroll_view_canvas)

            y_coord = 1
            frame_id = 1

            remove_item_img = Image.open("remove_item.png")
            remove_item_size = (50, 50)
            remove_item_img = remove_item_img.resize(remove_item_size)
            remove_item_ren = ImageTk.PhotoImage(remove_item_img)

            cart_subtotal_label = Label(self.view_cart_scr, text = "Cart Subtotal :- ", font = ("Arial", 20))
            cart_subtotal_label.place(x = 500, y = 650)

            if len(cart_items) == 0:
                cart_empty_label = Label(view_cart_frame, text = "CART EMPTY!", font = ('times', 25), fg = 'orange red')
                cart_empty_label.pack(side = RIGHT)
                checkout_button.configure(state=DISABLED)

            for cart_item in cart_items:
                product_id = cart_item[0]
                product_quantity = cart_item[1]

                get_product_info = "SELECT product_name, price, image_path FROM products_info WHERE id = %s"
                self.mycursor.execute(get_product_info, (product_id,))
                product_info_stage2 = self.mycursor.fetchall()
                product_info = product_info_stage2[0]
                product_name = product_info[0]
                product_price = product_info[1]
                product_image_path = product_info[2]

                self.product_display_frame = Frame(view_cart_frame, height = 250, width = 1350, bd = 12, relief = RIDGE)
                self.product_display_frame.grid(column = 0, row = y_coord)

                product_image = Image.open(product_image_path)
                product_image_size = (200, 200)
                product_image = product_image.resize(product_image_size)
                product_image_render = ImageTk.PhotoImage(product_image)

                product_image_label = Label(self.product_display_frame, image = product_image_render)
                product_image_label.image = product_image_render
                product_image_label.place(x = 0, y = 0)

                product_name_label = Label(self.product_display_frame, text = product_name, font = ('Nevrada', 20))
                product_name_label.place(x = 350, y = 50)

                product_quantity_label = Label(self.product_display_frame, text = "Quantity: " + str(product_quantity),
                                               font = ('Nevrada', 20))
                product_quantity_label.place(x = 350, y = 100)

                self.total_product_amount = int(product_price) * int(product_quantity)

                self.subtotal += self.total_product_amount
                product_amount_label = Label(self.product_display_frame, text = "Amount : " + str(self.total_product_amount),
                                             font = ('Nevrada', 20))
                product_amount_label.place(x = 700, y = 100)

                remove_item_button = Button(self.product_display_frame, image = remove_item_ren,
                                            command = partial(self.remove_item, product_id, self.view_cart_scr,
                                                              "view_cart"), bd = 0)
                remove_item_button.image = remove_item_ren
                remove_item_button.place(x = 1100, y = 80)

                y_coord += 1
                frame_id += 1

            locale.setlocale(locale.LC_ALL, 'en_US')
            self.subtotal_str = locale.format_string("%d", self.subtotal, grouping = True)
            cart_subtotal_label.config(text = "Cart Subtotal:-  (₹ " + str(self.subtotal_str) + ") Only")
        else:
            self.default_login("view")


class DisplaySuggestion(TheGanges, Entry):
    def __init__(self, searchable_items_list, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.searchable_items_list = searchable_items_list
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Escape>", self.esc)
        self.lb = None

        self.lb_up = False

    def esc(self, event):
        self.lb.destroy()
        if 'h' in ('q', 'w', 'a'):
            return event

    def changed(self, name, index, mode):
        if 'h' in ('q', 'w', 'a'):
            return name, index, mode

        if self.var.get() == '':
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox(width = 29, font = ('arial', 15))
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x = self.winfo_x(), y = self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)
        if 'h' in ('q', 'w', 'a'):
            return event

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first = index)
                index = str(int(index) - 1)
                self.lb.selection_set(first = index)
                self.lb.activate(index)
        if 'h' in ('q', 'w', 'a'):
            return event

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first = index)
                index = str(int(index) + 1)
                self.lb.selection_set(first = index)
                self.lb.activate(index)
        if 'h' in ('q', 'w', 'a'):
            return event

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + ".*")
        return [w for w in self.searchable_items_list if re.match(pattern, w)]


if __name__ == "__main__":
    root = Tk()  # makes window
    run_app = TheGanges(root)
    root.mainloop()  # for constant updates
