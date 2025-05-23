import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
import os
import time
from contact_manager import ContactManager
from PIL import Image, ImageTk  # 이미지 처리를 위한 Pillow 라이브러리


class ContactDialog(tk.Toplevel):
    """연락처 정보 입력 대화상자"""
    
    def __init__(self, parent, contact_manager, title="새 연락처", contact=None, theme="light"):
        """
        연락처 정보 입력 대화상자 초기화
        
        Args:
            parent: 부모 윈도우
            contact_manager: 연락처 관리자
            title: 대화상자 제목
            contact: 수정할 연락처 정보 (None인 경우 새 연락처 추가)
            theme: 테마 (light 또는 dark)
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(parent)  # 부모 윈도우에 종속
        self.grab_set()  # 모달 대화상자로 설정
        
        # 부모 윈도우의 핸드라이팅 폰트 가져오기 (제목용)
        if hasattr(parent, 'handwriting_font'):
            self.handwriting_font = parent.handwriting_font
        else:
            self.handwriting_font = "Arial"
        
        self.contact_manager = contact_manager
        self.contact = contact
        self.result = False
        self.theme = theme

        # 스타일 설정
        self.style = ttk.Style()
        
        if self.theme == "light":
            # 라이트 테마
            bg_color = "#f5f7fa"
            fg_color = "#2c3e50"
            button_bg = "#3498db"
            button_fg = "white"
            save_bg = "#2ecc71"
            status_bg = "#ecf0f1"
        else:  # dark 테마
            bg_color = "#2c3e50"
            fg_color = "#ecf0f1"
            button_bg = "#3498db"
            button_fg = "#ecf0f1"
            save_bg = "#27ae60"
            status_bg = "#2c3e50"
        
        self.style.configure("Dialog.TFrame", background=bg_color)
        self.style.configure("Dialog.TLabel", background=bg_color, foreground=fg_color, font=('Arial', 11))
        self.style.configure("Dialog.TButton", font=('Arial', 11, 'bold'), padding=6)
        
        # 저장 버튼 스타일
        self.style.configure("Save.TButton", background=save_bg, foreground=button_fg)
        self.style.map("Save.TButton", 
                      background=[('active', '#27ae60'), ('pressed', '#219653')])
        
        # 배경색 설정
        self.configure(background=bg_color)
        
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
        """대화상자 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self, padding="20", style="Dialog.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 이름 입력 필드
        name_label = ttk.Label(main_frame, text="이름:", style="Dialog.TLabel")
        name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, 
                              font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=10)
        name_entry.focus_set()  # 포커스 설정
        
        # 전화번호 입력 필드
        phone_label = ttk.Label(main_frame, text="전화번호:", style="Dialog.TLabel")
        phone_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(main_frame, textvariable=self.phone_var, 
                               font=('Arial', 11), width=30)
        phone_entry.grid(row=1, column=1, sticky=tk.EW, pady=10)
        
        # 그룹 선택 (콤보박스)
        group_label = ttk.Label(main_frame, text="그룹:", style="Dialog.TLabel")
        group_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.group_values = ("가족", "친구", "기타")
        self.group_var = tk.StringVar()
        if self.contact:
            self.group_var.set(self.contact["group"])
        else:
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
        self.root.title("ContactBook 📝")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 테마 설정 (기본값: light)
        self.theme = tk.StringVar(value="light")
        
        # 테마 설정
        self.style = ttk.Style()
        try:
            # 테마 설정 시도
            self.style.theme_use("clam")
        except tk.TclError:
            # macOS나 Linux에서는 기본 테마 사용
            pass
        
        # 사용 가능한 폰트 확인 및 손글씨 스타일 폰트 선택
        available_fonts = font.families()
        
        # 디버깅: 사용 가능한 모든 폰트 출력
        print("=== 사용 가능한 모든 폰트 ===")
        for f in sorted(available_fonts):
            print(f)
        print("===========================")
        
        # 한글 손글씨 폰트 목록 (Mac에서 사용 가능한 폰트)
        korean_handwriting_fonts = [
            # 동글동글한 느낌의 폰트를 우선 배치
            "Nanum Pen Script", "Nanum Brush Script", "NanumPen", "NanumBarunpen",
            "KCC-eunyoung", "KCC-Ganpan", "KCC-Hanbit",
            # 일반 한글 폰트
            "AppleSDGothicNeo-Regular", "AppleSDGothicNeo-Bold",
            "NanumMyeongjo", "Nanum Gothic", "Nanum Myeongjo",
            "KoPubBatang", "KoPubDotum", 
            "HanSans", "NanumGothic", 
            "AppleGothic", "Gungsuh", "HYGothic", "HCR Batang", "HCR Dotum",
            "Noto Sans KR", "Noto Serif KR", "Spoqa Han Sans", "Yoon Gothic",
            "Yoon Myungjo"
        ]
        
        # 영문 손글씨 폰트 목록
        english_handwriting_fonts = [
            "Comic Sans MS", "Brush Script MT", "Bradley Hand", "Chalkboard", 
            "Marker Felt", "Noteworthy", "Herculanum", "Papyrus", "Snell Roundhand"
        ]
        
        # 먼저 한글 폰트 확인
        self.handwriting_font = None
        for f in korean_handwriting_fonts:
            if f in available_fonts:
                self.handwriting_font = f
                print(f"선택된 한글 폰트: {f}")  # 디버깅용 출력
                break
        
        # 한글 폰트가 없으면 영문 폰트 확인
        if not self.handwriting_font:
            for f in english_handwriting_fonts:
                if f in available_fonts:
                    self.handwriting_font = f
                    print(f"선택된 영문 폰트: {f}")  # 디버깅용 출력
                    break
        
        # 손글씨 폰트가 없으면 기본 폰트 사용
        if not self.handwriting_font:
            self.handwriting_font = "Arial"
            print("기본 폰트 사용: Arial")  # 디버깅용 출력
        
        # 커스텀 폰트 설정
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        self.root.option_add("*Font", default_font)
        
        # 스타일 설정 (초기 테마 적용)
        self.apply_theme()
        
        # 연락처 관리자 초기화
        self.contact_manager = ContactManager()
        
        # 메인 프레임 생성
        self.create_widgets()
        
        # 연락처 목록 로드
        self.load_contacts()
        
        # 상태 표시줄 업데이트 시작
        self.update_status_bar()
    
    def apply_theme(self):
        """현재 테마 적용"""
        if self.theme.get() == "light":
            # 라이트 테마
            bg_color = "#f5f7fa"
            fg_color = "#2c3e50"
            button_bg = "#3498db"
            button_fg = "white"
            add_bg = "#2ecc71"
            delete_bg = "#e74c3c"
            tree_bg = "#ffffff"
            tree_fg = "#2c3e50"
            status_bg = "#e0e0e0"
            title_color = "#2c3e50"
        else:
            # 다크 테마
            bg_color = "#2c3e50"
            fg_color = "#ecf0f1"
            button_bg = "#3498db"
            button_fg = "#ecf0f1"
            add_bg = "#27ae60"
            delete_bg = "#c0392b"
            tree_bg = "#34495e"
            tree_fg = "#ecf0f1"
            status_bg = "#34495e"
            title_color = "#ecf0f1"
        
        # 기본 스타일
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", 
                            background=bg_color, 
                            foreground=fg_color, 
                            font=('Arial', 11))
        
        self.style.configure("TButton", 
                            font=('Arial', 11, 'bold'), 
                            padding=6, 
                            background=button_bg, 
                            foreground=button_fg)
        
        self.style.map('TButton', 
                       background=[('active', '#2980b9'), ('pressed', '#2471a3')],
                       foreground=[('active', button_fg), ('pressed', button_fg)])
        
        # 트리뷰 스타일
        self.style.configure("Treeview", 
                            font=('Arial', 10), 
                            rowheight=25, 
                            background=tree_bg, 
                            foreground=tree_fg, 
                            fieldbackground=tree_bg)
        
        self.style.configure("Treeview.Heading", 
                            font=('Arial', 11, 'bold'), 
                            background=bg_color, 
                            foreground=fg_color)
        
        # 커스텀 버튼 스타일
        self.style.configure("Add.TButton", background=add_bg, foreground=button_fg)
        self.style.map("Add.TButton", 
                       background=[('active', '#27ae60'), ('pressed', '#219653')])
        
        self.style.configure("Delete.TButton", background=delete_bg, foreground=button_fg)
        self.style.map("Delete.TButton", 
                       background=[('active', '#c0392b'), ('pressed', '#a93226')])
        
        # 헤더 스타일
        self.style.configure("Header.TLabel", 
                            font=('Arial', 20, 'bold'), 
                            foreground=fg_color,
                            background=bg_color)
        
        # 노트 스타일 제목 (손글씨 효과)
        self.style.configure("Note.TLabel", 
                           font=(self.handwriting_font, 28, 'bold'), 
                           foreground=title_color,
                           background=bg_color)
        
        # 상태 표시줄 스타일
        self.style.configure("Status.TLabel", 
                           background=status_bg, 
                           foreground=fg_color, 
                           font=('Arial', 9))
        
        # 배경색 설정
        self.root.configure(background=bg_color)
        
        # 이미 생성된 위젯이 있으면 업데이트
        if hasattr(self, 'main_frame'):
            self.main_frame.configure(style="TFrame")
            self.title_label.configure(style="Note.TLabel")
            self.status_label.configure(style="Status.TLabel")
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 프레임
        self.main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목 및 테마 전환 프레임
        title_frame = ttk.Frame(self.main_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 빈 공간으로 중앙 정렬 효과 만들기
        ttk.Label(title_frame, text="", style="TLabel").pack(side=tk.LEFT, expand=True)
        
        # 제목 레이블 
        self.title_label = ttk.Label(title_frame, text="ContactBook 📝", 
                                   font=(self.handwriting_font, 28, 'bold'), 
                                   foreground="#3498db",
                                   style="Note.TLabel")
        self.title_label.pack(side=tk.LEFT)
        
        # 빈 공간으로 중앙 정렬 효과 만들기
        ttk.Label(title_frame, text="", style="TLabel").pack(side=tk.LEFT, expand=True)
        
        # 테마 전환 버튼
        theme_frame = ttk.Frame(title_frame, style="TFrame")
        theme_frame.pack(side=tk.RIGHT)
        
        light_radio = ttk.Radiobutton(theme_frame, text="라이트", 
                                     variable=self.theme, 
                                     value="light", 
                                     command=self.apply_theme)
        light_radio.pack(side=tk.LEFT, padx=5)
        
        dark_radio = ttk.Radiobutton(theme_frame, text="다크", 
                                    variable=self.theme, 
                                    value="dark", 
                                    command=self.apply_theme)
        dark_radio.pack(side=tk.LEFT, padx=5)
        
        # 구분선 추가
        separator = ttk.Separator(self.main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=(0, 20))
        
        # 검색 및 추가 프레임
        search_frame = ttk.Frame(self.main_frame, style="TFrame")
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
        list_label = ttk.Label(self.main_frame, text="연락처 목록", 
                              font=('Arial', 12, 'bold'), 
                              foreground="#2c3e50",
                              style="TLabel")
        list_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 연락처 목록 프레임
        list_frame = ttk.Frame(self.main_frame, style="TFrame")
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
        
        # 상태 표시줄 추가
        self.status_label = ttk.Label(self.root, text="준비 완료", style="Status.TLabel", anchor=tk.W, padding=(10, 8))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def show_add_dialog(self):
        """새 연락처 추가 대화상자 표시"""
        dialog = ContactDialog(self.root, self.contact_manager, "새 연락처", theme=self.theme.get())
        self.root.wait_window(dialog)
        
        # 연락처가 추가되었으면 목록 새로고침
        if dialog.result:
            self.load_contacts()
            self.status_label.config(text="새 연락처가 추가되었습니다.")
    
    def show_edit_dialog(self, contact):
        """연락처 수정 대화상자 표시"""
        dialog = ContactDialog(self.root, self.contact_manager, "연락처 수정", contact, theme=self.theme.get())
        self.root.wait_window(dialog)
        
        # 연락처가 수정되었으면 목록 새로고침
        if dialog.result:
            self.load_contacts()
            self.status_label.config(text="연락처가 수정되었습니다.")
    
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
    
    def update_status_bar(self):
        """상태 표시줄 업데이트"""
        # 현재 시간 표시
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        contact_count = len(self.contact_manager.get_all_contacts())
        status_text = f"연락처 수: {contact_count}  |  마지막 업데이트: {current_time}"
        self.status_label.config(text=status_text)
        
        # 1초마다 업데이트
        self.root.after(1000, self.update_status_bar)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
