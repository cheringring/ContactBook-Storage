import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
import os
from contact_manager import ContactManager
from PIL import Image, ImageTk  # 이미지 처리를 위한 Pillow 라이브러리


class ContactDialog(tk.Toplevel):
    """연락처 정보 입력 대화상자"""
    
    def __init__(self, parent, contact_manager, title="새 연락처", contact=None):
        """
        연락처 정보 입력 대화상자 초기화
        
        Args:
            parent: 부모 윈도우
            contact_manager: 연락처 관리자
            title: 대화상자 제목
            contact: 수정할 연락처 정보 (None인 경우 새 연락처 추가)
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.contact_manager = contact_manager
        self.contact = contact
        self.result = False
        
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure("Dialog.TFrame", background="#f5f7fa")
        self.style.configure("Dialog.TLabel", background="#f5f7fa", font=('Arial', 11))
        self.style.configure("Dialog.TButton", font=('Arial', 11, 'bold'), padding=6)
        
        # 저장 버튼 스타일
        self.style.configure("Save.TButton", background="#2ecc71", foreground="white")
        self.style.map("Save.TButton", 
                      background=[('active', '#27ae60'), ('pressed', '#219653')])
        
        # 배경색 설정
        self.configure(background="#f5f7fa")
        
        self.create_widgets()
        self.center_window()
        
        # ESC 키 누르면 창 닫기
        self.bind("<Escape>", lambda event: self.destroy())
        
        # 기존 연락처 정보 설정
        if contact:
            self.name_var.set(contact["name"])
            self.phone_var.set(contact["phone"])
            self.group_var.set(contact["group"])
            self.original_phone = contact["phone"]
        else:
            self.original_phone = None
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self, padding="20", style="Dialog.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 이름 입력
        name_label = ttk.Label(main_frame, text="이름:", style="Dialog.TLabel")
        name_label.grid(row=0, column=0, sticky=tk.W, pady=10)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, 
                              font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=10)
        name_entry.focus_set()  # 포커스 설정
        
        # 전화번호 입력
        phone_label = ttk.Label(main_frame, text="전화번호:", style="Dialog.TLabel")
        phone_label.grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(main_frame, textvariable=self.phone_var, 
                               font=('Arial', 11), width=30)
        phone_entry.grid(row=1, column=1, sticky=tk.EW, pady=10)
        
        # 그룹 선택 (콤보박스)
        group_label = ttk.Label(main_frame, text="그룹:", style="Dialog.TLabel")
        group_label.grid(row=2, column=0, sticky=tk.W, pady=10)
        
        self.group_var = tk.StringVar()
        self.group_values = ["가족", "친구", "기타"]
        self.group_var.set("기타")  # 기본값
        
        group_combobox = ttk.Combobox(main_frame, 
                                     textvariable=self.group_var,
                                     values=self.group_values,
                                     state="readonly",
                                     font=('Arial', 11),
                                     width=28)
        group_combobox.grid(row=2, column=1, sticky=tk.EW, pady=10)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame, style="Dialog.TFrame")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # 저장 버튼
        save_button = ttk.Button(button_frame, text="저장", 
                                command=self.save_contact, 
                                style="Save.TButton", 
                                width=12)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 취소 버튼
        cancel_button = ttk.Button(button_frame, text="취소", 
                                  command=self.destroy, 
                                  width=12)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # 컬럼 확장 설정
        main_frame.columnconfigure(1, weight=1)
        
        # Enter 키 누르면 저장
        self.bind("<Return>", lambda event: self.save_contact())
    
    def save_contact(self):
        """연락처 저장"""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        group = self.group_var.get()
        
        # 필수 필드 검증
        if not name or not phone:
            messagebox.showerror("오류", "이름과 전화번호는 필수 입력 항목입니다.", parent=self)
            return
        
        # 수정 또는 추가
        if self.original_phone:
            # 연락처 수정
            success = self.contact_manager.update_contact(
                self.original_phone, name, phone, group
            )
            
            if success:
                messagebox.showinfo("성공", "연락처가 수정되었습니다.", parent=self)
                self.result = True
                self.destroy()
            else:
                messagebox.showerror("오류", "이미 존재하는 전화번호입니다.", parent=self)
        else:
            # 새 연락처 추가
            success = self.contact_manager.add_contact(name, phone, group)
            
            if success:
                messagebox.showinfo("성공", "새 연락처가 추가되었습니다.", parent=self)
                self.result = True
                self.destroy()
            else:
                messagebox.showerror("오류", "이미 존재하는 전화번호입니다.", parent=self)
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


class ContactBookApp:
    """전화번호부 GUI 애플리케이션"""
    
    def __init__(self, root):
        """
        애플리케이션 초기화
        
        Args:
            root: Tkinter 루트 윈도우
        """
        self.root = root
        self.root.title("연락처 관리 시스템")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 테마 설정
        self.style = ttk.Style()
        try:
            # Windows에서는 'vista' 테마를 사용
            self.style.theme_use('clam')
        except tk.TclError:
            # macOS나 Linux에서는 기본 테마 사용
            pass
        
        # 커스텀 폰트 설정
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        self.root.option_add("*Font", default_font)
        
        # 스타일 설정
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("TLabel", background="#f5f7fa", font=('Arial', 11))
        self.style.configure("TButton", font=('Arial', 11, 'bold'), padding=6)
        self.style.map('TButton', 
                       background=[('active', '#3498db'), ('pressed', '#2980b9')],
                       foreground=[('active', 'white'), ('pressed', 'white')])
        self.style.configure("Treeview", font=('Arial', 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        
        # 커스텀 버튼 스타일
        self.style.configure("Add.TButton", background="#2ecc71", foreground="white")
        self.style.map("Add.TButton", 
                       background=[('active', '#27ae60'), ('pressed', '#219653')])
        
        self.style.configure("Delete.TButton", background="#e74c3c", foreground="white")
        self.style.map("Delete.TButton", 
                       background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        # 헤더 스타일
        self.style.configure("Header.TLabel", 
                            font=('Arial', 20, 'bold'), 
                            foreground="#2c3e50",
                            background="#f5f7fa")
        
        # 배경색 설정
        self.root.configure(background="#f5f7fa")
        
        # 연락처 관리자 초기화
        self.contact_manager = ContactManager()
        
        # 메인 프레임 생성
        self.create_widgets()
        
        # 연락처 목록 로드
        self.load_contacts()
        
        # 애니메이션 효과 시작
        self.animate_title()
    
    def animate_title(self):
        """제목 애니메이션 효과"""
        colors = ["#3498db", "#2980b9", "#1abc9c", "#16a085", "#2ecc71", "#27ae60"]
        current_color = self.title_label.cget("foreground")
        
        # 색상 순환
        next_index = (colors.index(current_color) + 1) % len(colors) if current_color in colors else 0
        next_color = colors[next_index]
        
        # 색상 변경
        self.title_label.configure(foreground=next_color)
        
        # 1초 후 다시 호출
        self.root.after(2000, self.animate_title)
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목 프레임
        title_frame = ttk.Frame(main_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 빈 공간으로 중앙 정렬 효과 만들기
        ttk.Label(title_frame, text="", style="TLabel").pack(side=tk.LEFT, expand=True)
        
        # 제목 레이블 (그라데이션 효과는 애니메이션으로 구현)
        self.title_label = ttk.Label(title_frame, text="연락처 관리 시스템", 
                                   font=('Arial', 24, 'bold'), 
                                   foreground="#3498db",
                                   style="Header.TLabel")
        self.title_label.pack(side=tk.LEFT)
        
        # 빈 공간으로 중앙 정렬 효과 만들기
        ttk.Label(title_frame, text="", style="TLabel").pack(side=tk.LEFT, expand=True)
        
        # 구분선 추가
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # 검색 및 추가 프레임
        search_frame = ttk.Frame(main_frame, style="TFrame")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 검색 레이블 및 입력 필드
        search_label = ttk.Label(search_frame, text="검색:", style="TLabel")
        search_label.pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                font=('Arial', 11), width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 추가 버튼
        add_button = ttk.Button(search_frame, text="추가", 
                               command=self.show_add_dialog, 
                               style="Add.TButton", 
                               width=8)
        add_button.pack(side=tk.RIGHT, padx=5)
        
        # 연락처 목록 레이블
        list_label = ttk.Label(main_frame, text="연락처 목록", 
                              font=('Arial', 12, 'bold'), 
                              foreground="#2c3e50",
                              style="TLabel")
        list_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 연락처 목록 프레임
        list_frame = ttk.Frame(main_frame, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 연락처 목록 트리뷰
        columns = ("name", "phone", "group")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Treeview")
        
        # 컬럼 설정
        self.tree.heading("name", text="이름")
        self.tree.heading("phone", text="전화번호")
        self.tree.heading("group", text="그룹")
        
        self.tree.column("name", width=150)
        self.tree.column("phone", width=150)
        self.tree.column("group", width=100)
        
        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 오른쪽 마우스 클릭 이벤트 바인딩
        self.tree.bind("<Button-3>", self.show_context_menu)
        # 더블 클릭 이벤트 바인딩
        self.tree.bind("<Double-1>", self.on_double_click)
    
    def show_add_dialog(self):
        """새 연락처 추가 대화상자 표시"""
        dialog = ContactDialog(self.root, self.contact_manager, "새 연락처")
        self.root.wait_window(dialog)
        
        # 연락처가 추가되었으면 목록 새로고침
        if dialog.result:
            self.load_contacts()
    
    def show_edit_dialog(self, contact):
        """연락처 수정 대화상자 표시"""
        dialog = ContactDialog(self.root, self.contact_manager, "연락처 수정", contact)
        self.root.wait_window(dialog)
        
        # 연락처가 수정되었으면 목록 새로고침
        if dialog.result:
            self.load_contacts()
    
    def on_double_click(self, event):
        """연락처 더블 클릭 시 수정 대화상자 표시"""
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        # 선택한 항목의 정보 가져오기
        values = self.tree.item(item, "values")
        if not values:
            return
            
        # 연락처 정보 가져오기
        name, phone, group = values
        contact = {
            "name": name,
            "phone": phone,
            "group": group
        }
        
        # 수정 대화상자 표시
        self.show_edit_dialog(contact)
    
    def show_context_menu(self, event):
        """오른쪽 마우스 클릭 시 컨텍스트 메뉴 표시"""
        # 클릭한 위치의 항목 선택
        item = self.tree.identify_row(event.y)
        if not item:
            return
            
        # 항목 선택
        self.tree.selection_set(item)
        self.tree.focus(item)
        
        # 선택한 항목의 정보 가져오기
        values = self.tree.item(item, "values")
        if not values:
            return
            
        # 연락처 정보 가져오기
        name, phone, group = values
        contact = {
            "name": name,
            "phone": phone,
            "group": group
        }
        
        # 컨텍스트 메뉴 생성
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="변경", command=lambda: self.show_edit_dialog(contact))
        context_menu.add_command(label="출력", command=lambda: self.print_contact(values))
        context_menu.add_command(label="삭제", command=lambda: self.delete_contact(phone))
        
        # 메뉴 표시
        context_menu.post(event.x_root, event.y_root)
    
    def print_contact(self, values):
        """선택한 연락처 정보 출력"""
        if not values:
            return
            
        name, phone, group = values
        
        # 정보 창 표시
        info = f"이름: {name}\n전화번호: {phone}\n그룹: {group}"
        messagebox.showinfo("연락처 정보", info)
    
    def delete_contact(self, phone):
        """연락처 삭제"""
        # 삭제 확인
        if messagebox.askyesno("확인", "정말로 이 연락처를 삭제하시겠습니까?"):
            success = self.contact_manager.delete_contact(phone)
            
            if success:
                messagebox.showinfo("성공", "연락처가 삭제되었습니다.")
                self.load_contacts()
            else:
                messagebox.showerror("오류", "연락처 삭제 중 오류가 발생했습니다.")
    
    def load_contacts(self):
        """연락처 목록 로드"""
        # 기존 항목 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 연락처 추가
        contacts = self.contact_manager.get_all_contacts()
        for contact in contacts:
            self.tree.insert("", tk.END, values=(
                contact["name"],
                contact["phone"],
                contact["group"]
            ))
    
    def on_search(self, *args):
        """검색 기능"""
        keyword = self.search_var.get()
        
        # 기존 항목 삭제
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if keyword:
            # 검색 결과 표시
            results = self.contact_manager.search_contacts(keyword)
            for contact in results:
                self.tree.insert("", tk.END, values=(
                    contact["name"],
                    contact["phone"],
                    contact["group"]
                ))
        else:
            # 전체 목록 표시
            self.load_contacts()


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
