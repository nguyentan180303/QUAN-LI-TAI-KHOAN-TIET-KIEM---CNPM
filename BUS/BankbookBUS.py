from DAL.BankbookDAL import BankbookDAL

class BankbookBUS:
    def __init__(self):
        self.bankbook_dal = BankbookDAL()

    def insert_new_record(self, maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui):
        try:
            # Perform any necessary business logic or validation here
            if not maso or not loaitk or not khachhang or not cmnd or not diachi or not ngaymo or not sotiengui:
                print("All fields are required.")
                return False

            # Call the DAL layer to insert the record
            return self.bankbook_dal.insert_new_record(
                maso, loaitk, khachhang, cmnd, diachi, ngaymo, sotiengui
            )
        except Exception as e:
            print(f"Error in business layer: {e}")
            return False