import customtkinter as ctk
from BUS.Lookup_Bankbook_BUS import Lookup_Bankbook_BUS

class Lookup_Bankbook_GUI:
    def __init__(self, parent_frame):
        """Initialize the lookup bankbook GUI
        
        Args:
            parent_frame: The parent frame to attach this GUI to
        """
        self.parent_frame = parent_frame
        self.lookup_bankbook_bus = Lookup_Bankbook_BUS()
        self.create_screen_lookup_bankbook()
    
    def create_screen_lookup_bankbook(self):
        """Create the main lookup bankbook screen"""
        # Main container
        main_container = ctk.CTkFrame(self.parent_frame)
        main_container.pack(padx=20, pady=20, fill="both", expand=True)

        # Header and Title
        header_frame = ctk.CTkFrame(main_container, fg_color=("#1f538d"), border_width=1)
        header_frame.pack(fill="x")

        # Title with border
        title_frame = ctk.CTkFrame(header_frame, fg_color=("#1f538d"))
        title_frame.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        title_label = ctk.CTkLabel(title_frame, text="Danh Sách Sổ Tiết Kiệm", text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(padx=10, pady=5)

        # Search area
        search_frame = ctk.CTkFrame(main_container)
        search_frame.pack(fill="x", pady=10)

        # Account number input
        ma_so_frame = ctk.CTkFrame(search_frame)
        ma_so_frame.pack(side="left", padx=5)
        ma_so_label = ctk.CTkLabel(ma_so_frame, text="Mã số:")
        ma_so_label.pack(side="left", padx=5)
        self.ma_so_entry = ctk.CTkEntry(ma_so_frame, width=150)
        self.ma_so_entry.pack(side="left", padx=5)

        # Account type input
        loai_tk_frame = ctk.CTkFrame(search_frame)
        loai_tk_frame.pack(side="left", padx=5)
        loai_tk_label = ctk.CTkLabel(loai_tk_frame, text="Loại tiết kiệm:")
        loai_tk_label.pack(side="left", padx=5)
        self.loai_tk_var = ctk.StringVar(value="Tất cả")
        self.loai_tk_combo = ctk.CTkComboBox(
            loai_tk_frame, 
            width=150,
            values=["Tất cả", "3 tháng", "6 tháng", "Không kỳ hạn"],
            variable=self.loai_tk_var
        )
        self.loai_tk_combo.pack(side="left", padx=5)

        # Customer name input
        khach_hang_frame = ctk.CTkFrame(search_frame)
        khach_hang_frame.pack(side="left", padx=5)
        khach_hang_label = ctk.CTkLabel(khach_hang_frame, text="Khách hàng:")
        khach_hang_label.pack(side="left", padx=5)
        self.khach_hang_entry = ctk.CTkEntry(khach_hang_frame, width=150)
        self.khach_hang_entry.pack(side="left", padx=5)

        # Search button
        search_button = ctk.CTkButton(search_frame, text="Tìm kiếm", command=self.search_bankbooks)
        search_button.pack(side="left", padx=10)

        # Table container
        self.table_container = ctk.CTkFrame(main_container, border_width=1)
        self.table_container.pack(fill="both", expand=True, pady=(1, 0))

        # Headers row
        headers = ["STT", "Mã Số", "Loại Tiết Kiệm", "Khách Hàng", "Số Dư"]
        for col, header in enumerate(headers):
            header_frame = ctk.CTkFrame(self.table_container, fg_color=("#1f538d"), border_width=1)
            header_frame.grid(row=0, column=col, sticky="nsew", padx=(0,1), pady=(0,1))
            header_label = ctk.CTkLabel(header_frame, text=header, text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
            header_label.pack(padx=10, pady=5)

        # Configure column weights
        self.table_container.grid_columnconfigure(0, weight=1)  # Serial number
        self.table_container.grid_columnconfigure(1, weight=2)  # Account number
        self.table_container.grid_columnconfigure(2, weight=2)  # Account type
        self.table_container.grid_columnconfigure(3, weight=3)  # Customer name
        self.table_container.grid_columnconfigure(4, weight=2)  # Balance

        # Populate the table with initial data
        self.populate_table()

    def search_bankbooks(self):
        """Search bankbooks based on input criteria"""
        try:
            # Get search criteria
            ma_so = self.ma_so_entry.get().strip()
            loai_tk = self.loai_tk_var.get()
            if loai_tk == "Tất cả":
                loai_tk = ""
            khach_hang = self.khach_hang_entry.get().strip()

            # Fetch filtered data from the business layer
            data = self.lookup_bankbook_bus.search_bankbooks(ma_so, loai_tk, khach_hang)

            # Clear existing table data
            self.clear_table()

            # Populate the table with filtered data
            for row_index, row in enumerate(data):
                for col_index, value in enumerate(row.values()):
                    cell_frame = ctk.CTkFrame(self.table_container, border_width=0)
                    cell_frame.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=(0, 1), pady=(0, 1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(value))
                    cell_label.pack(padx=10, pady=8)

        except Exception as e:
            print(f"Error searching bankbooks: {e}")

    def clear_table(self):
        """Clear all data rows from the table while keeping headers"""
        # Remove all widgets except headers (row 0)
        for widget in self.table_container.grid_slaves():
            if int(widget.grid_info()['row']) > 0:
                widget.destroy()
        self.table_container.update()

    def populate_table(self):
        """Populate the table with all bankbook data"""
        try:
            # Fetch data from the business layer
            data = self.lookup_bankbook_bus.get_all_bankbooks()

            # Populate the table with data
            for row_index, row in enumerate(data):
                for col_index, value in enumerate(row.values()):
                    cell_frame = ctk.CTkFrame(self.table_container, border_width=0)
                    cell_frame.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=(0, 1), pady=(0, 1))
                    cell_label = ctk.CTkLabel(cell_frame, text=str(value))
                    cell_label.pack(padx=10, pady=8)

        except Exception as e:
            print(f"Error populating table: {e}")