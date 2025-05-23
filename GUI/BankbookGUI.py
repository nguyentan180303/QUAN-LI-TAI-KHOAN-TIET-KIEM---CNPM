import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import tkinter as tk
import Create_deposit_slip_GUI
import Create_withdrawal_slip_GUI
import Lookup_Bankbook_GUI
import Prepare_monthly_report_GUI
from utils.db_utils import DatabaseConnection
from BUS.BankbookBUS import BankbookBUS


class BankbookGUI(ctk.CTk):
    def __init__(self, user_id, username, password):
        super().__init__()

        # Store user information
        self.user_id = user_id
        self.username = username
        self.password = password
        self.db = DatabaseConnection()
        self.bankbook_bus = BankbookBUS()

        # Configure window
        self.title("Quản Lý Sổ Tiết Kiệm")
        self.geometry("800x600")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left frame for navigation
        self.left_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Account information section
        self.account_detail_label = ctk.CTkLabel(self.left_frame, text="Thông Tin Tài Khoản:", font=ctk.CTkFont(size=18, weight="bold"))
        self.account_detail_label.pack(pady=20)

        self.account_label = ctk.CTkLabel(self.left_frame, text=f"Tài khoản: {self.username}")
        self.account_label.pack(pady=5)

        self.id_account_label = ctk.CTkLabel(self.left_frame, text=f"ID: {self.user_id}")
        self.id_account_label.pack(pady=5)

        # Navigation buttons
        self.create_bankbook_button = ctk.CTkButton(self.left_frame, text="Mở sổ tiết kiệm", command=self.create_bankbook)
        self.create_bankbook_button.pack(pady=10)

        self.create_deposit_slip_button = ctk.CTkButton(self.left_frame, text="Lập phiếu gửi tiền", command=self.create_deposit_slip)
        self.create_deposit_slip_button.pack(pady=10)

        self.create_withdrawal_slip_button = ctk.CTkButton(self.left_frame, text="Lập phiếu rút tiền", command=self.create_withdrawal_slip)
        self.create_withdrawal_slip_button.pack(pady=10)

        self.lookup_bankbook_button = ctk.CTkButton(self.left_frame, text="Tra cứu sổ", command=self.lookup_bankbook)
        self.lookup_bankbook_button.pack(pady=10)

        self.prepare_monthly_report_button = ctk.CTkButton(self.left_frame, text="Lập báo cáo tháng", command=self.prepare_monthly_report)
        self.prepare_monthly_report_button.pack(pady=10)

        self.change_rules_button = ctk.CTkButton(self.left_frame, text="Thay đổi quy định", command=self.change_rules)
        self.change_rules_button.pack(pady=10)

        # Right frame for content
        self.right_frame = ctk.CTkFrame(self, corner_radius=0)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Display default screen
        self.create_bankbook()

    def clear_right_frame(self):
        """Clear all widgets in the right frame"""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def create_bankbook(self):
        """Display the form for creating a new savings account"""
        self.clear_right_frame()

        # Title
        title_label = ctk.CTkLabel(self.right_frame, text="Mở Sổ Tiết Kiệm", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)

        # Main form
        form_frame = ctk.CTkFrame(self.right_frame)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Account number and type
        row1_frame = ctk.CTkFrame(form_frame)
        row1_frame.pack(fill="x", padx=10, pady=5)
        
        maso_label = ctk.CTkLabel(row1_frame, text="Mã số:")
        maso_label.pack(side="left", padx=5)
        self.maso_entry = ctk.CTkEntry(row1_frame)
        self.maso_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        loaitk_label = ctk.CTkLabel(row1_frame, text="Loại tiết kiệm:")
        loaitk_label.pack(side="left", padx=5)
        self.selected_option = ctk.StringVar(value="3 tháng")
        options = ["3 tháng", "6 tháng", "Không kỳ hạn"]
        dropdown = ctk.CTkOptionMenu(row1_frame, variable=self.selected_option, text_color="black", fg_color="#F5F5F5", values=options)
        dropdown.pack(side="left", expand=True, fill="x", pady=5)

        # Customer information
        row2_frame = ctk.CTkFrame(form_frame)
        row2_frame.pack(fill="x", padx=10, pady=5)
        
        khachhang_label = ctk.CTkLabel(row2_frame, text="Khách hàng:")
        khachhang_label.pack(side="left", padx=5)
        self.khachhang_entry = ctk.CTkEntry(row2_frame)
        self.khachhang_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        cmnd_label = ctk.CTkLabel(row2_frame, text="CMND:")
        cmnd_label.pack(side="left", padx=5)
        self.cmnd_entry = ctk.CTkEntry(row2_frame)
        self.cmnd_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Address
        row3_frame = ctk.CTkFrame(form_frame)
        row3_frame.pack(fill="x", padx=10, pady=5)
        
        diachi_label = ctk.CTkLabel(row3_frame, text="Địa chỉ:")
        diachi_label.pack(side="left", padx=5)
        self.diachi_entry = ctk.CTkEntry(row3_frame)
        self.diachi_entry.pack(side="left", expand=True, fill="x", padx=5)

        # Opening date
        row4_frame = ctk.CTkFrame(form_frame)
        row4_frame.pack(fill="x", padx=10, pady=5)
        current_date = datetime.now()

        ngaymo_label = ctk.CTkLabel(row4_frame, text="Ngày mở sổ:")
        ngaymo_label.pack(side="left", padx=5)
        self.ngaymo_entry = ctk.CTkEntry(row4_frame)
        self.ngaymo_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.ngaymo_entry.insert(0, current_date.strftime("%d/%m/%Y"))
        
        # Deposit amount
        row5_frame = ctk.CTkFrame(form_frame)
        row5_frame.pack(fill="x", padx=10, pady=5)

        sotiengui_label = ctk.CTkLabel(row5_frame, text="Số tiền gửi:")
        sotiengui_label.pack(side="left", padx=5)
        self.sotiengui_entry = ctk.CTkEntry(row5_frame)
        self.sotiengui_entry.pack(side="left", expand=True, fill="x", padx=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.right_frame)
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(button_frame, text="Lưu", command=self.insert_new_record)
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Hủy", command=self.clear_bankbook_fields)
        cancel_button.pack(side="left", padx=10)

    def insert_new_record(self):
        """Insert a new savings account record"""
        try:
            # Get form data
            maso = self.maso_entry.get()
            loaitk = self.selected_option.get()
            khachhang = self.khachhang_entry.get()
            cmnd = self.cmnd_entry.get()
            diachi = self.diachi_entry.get()
            ngaymo = self.ngaymo_entry.get()
            sotiengui = self.sotiengui_entry.get()
            
            # Validate ID number
            if self.checkCMND(cmnd):
                messagebox.showerror("Lỗi", "CMND đã tồn tại trong hệ thống!")
                self.cmnd_entry.focus()
                return
            
            # Validate account number
            if self.checkmaso(maso):
                messagebox.showerror("Lỗi", "Mã số đã tồn tại trong hệ thống!")
                self.maso_entry.focus()
                return

            # Validate minimum deposit amount
            try:
                value = float(self.sotiengui_entry.get().replace(",", ""))
                if value < 1000000:
                    messagebox.showerror("Lỗi", "Số tiền phải lớn hơn hoặc bằng 1,000,000!")
                    self.sotiengui_entry.focus()        
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ!")
                self.sotiengui_entry.focus()
                return

            # Insert record
            result = self.bankbook_bus.insert_new_record(
                maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui
            )

            if result:
                messagebox.showinfo("Thành công", "Mở sổ tiết kiệm thành công")
            else:
                messagebox.showerror("Lỗi", "Không thể mở sổ tiết kiệm")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def clear_bankbook_fields(self):
        """Clear all form fields"""
        try:
            self.maso_entry.delete(0, "end")
            self.khachhang_entry.delete(0, "end")
            self.cmnd_entry.delete(0, "end")
            self.diachi_entry.delete(0, "end")
            self.ngaymo_entry.delete(0, "end")
            self.sotiengui_entry.delete(0, "end")
        except Exception as e:
            print(f"Error clearing fields: {e}")

    def create_deposit_slip(self):
        """Display deposit slip creation screen"""
        self.clear_right_frame()
        Create_deposit_slip_GUI.Create_deposit_slip_GUI(self.right_frame)

    def create_withdrawal_slip(self):
        """Display withdrawal slip creation screen"""
        self.clear_right_frame()
        Create_withdrawal_slip_GUI.Create_withdrawal_slip_GUI(self.right_frame)
    
    def lookup_bankbook(self):
        """Display account lookup screen"""
        self.clear_right_frame()
        self.geometry("1200x800")  # Resize window for lookup screen
        Lookup_Bankbook_GUI.Lookup_Bankbook_GUI(self.right_frame)
    
    def prepare_monthly_report(self):
        """Display monthly report generation screen"""
        self.clear_right_frame()
        Prepare_monthly_report_GUI.Prepare_monthly_report_GUI(self.right_frame)
    
    def checkCMND(self, cmnd):
        """Check if ID number already exists"""
        if cmnd:
            try:
                connection = self.db.connect()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM SoTietKiem WHERE CMND = ?", (cmnd,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"Error checking ID number: {e}")
                return False
        
    def checkmaso(self, maso):
        """Check if account number already exists"""
        if maso:
            try:
                connection = self.db.connect()
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM SoTietKiem WHERE maSo = ?", (maso,))
                count = cursor.fetchone()[0]
                return count > 0
            except Exception as e:
                print(f"Error checking account number: {e}")
                return False        

    def change_rules(self):
        """Display rules change screen"""
        self.clear_right_frame()
        Change_rules_GUI.Change_rules_GUI(self.right_frame)

    
# if __name__ == "__main__":
#     app = BankbookGUI()
#     app.mainloop()