import json
import os
from typing import Dict, List, Optional


class ContactManager:
    """연락처 관리 클래스"""
    
    def __init__(self, file_path: str = "contacts.json"):
        """
        ContactManager 초기화
        
        Args:
            file_path: 연락처 데이터를 저장할 파일 경로
        """
        self.file_path = file_path
        self.contacts = []
        self.load_contacts()
    
    def load_contacts(self) -> None:
        """파일에서 연락처 데이터 불러오기"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
            except json.JSONDecodeError:
                self.contacts = []
        else:
            self.contacts = []
    
    def save_contacts(self) -> None:
        """연락처 데이터를 파일에 저장"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.contacts, file, ensure_ascii=False, indent=2)
    
    def add_contact(self, name: str, phone: str, group: str = "기타") -> bool:
        """
        새 연락처 추가
        
        Args:
            name: 이름
            phone: 전화번호
            group: 그룹 (가족, 친구, 기타)
            
        Returns:
            성공 여부
        """
        # 이미 존재하는 전화번호인지 확인
        if self.find_contact_by_phone(phone):
            return False
            
        contact = {
            "name": name,
            "phone": phone,
            "group": group
        }
        
        self.contacts.append(contact)
        self.save_contacts()
        return True
    
    def delete_contact(self, phone: str) -> bool:
        """
        연락처 삭제
        
        Args:
            phone: 삭제할 연락처의 전화번호
            
        Returns:
            성공 여부
        """
        for i, contact in enumerate(self.contacts):
            if contact["phone"] == phone:
                del self.contacts[i]
                self.save_contacts()
                return True
        return False
    
    def update_contact(self, old_phone: str, name: str, phone: str, group: str) -> bool:
        """
        연락처 수정
        
        Args:
            old_phone: 수정할 연락처의 기존 전화번호
            name: 새 이름
            phone: 새 전화번호
            group: 새 그룹
            
        Returns:
            성공 여부
        """
        # 전화번호가 변경되었고, 새 전화번호가 이미 존재하는 경우
        if old_phone != phone and self.find_contact_by_phone(phone):
            return False
            
        for i, contact in enumerate(self.contacts):
            if contact["phone"] == old_phone:
                self.contacts[i] = {
                    "name": name,
                    "phone": phone,
                    "group": group
                }
                self.save_contacts()
                return True
        return False
    
    def find_contact_by_phone(self, phone: str) -> Optional[Dict]:
        """
        전화번호로 연락처 검색
        
        Args:
            phone: 검색할 전화번호
            
        Returns:
            찾은 연락처 또는 None
        """
        for contact in self.contacts:
            if contact["phone"] == phone:
                return contact
        return None
    
    def search_contacts(self, keyword: str) -> List[Dict]:
        """
        키워드로 연락처 검색
        
        Args:
            keyword: 검색 키워드 (이름, 전화번호, 그룹에서 검색)
            
        Returns:
            검색된 연락처 목록
        """
        keyword = keyword.lower()
        results = []
        
        for contact in self.contacts:
            if (keyword in contact["name"].lower() or 
                keyword in contact["phone"].lower() or 
                keyword in contact["group"].lower()):
                results.append(contact)
                
        return results
    
    def get_all_contacts(self) -> List[Dict]:
        """
        모든 연락처 반환
        
        Returns:
            모든 연락처 목록
        """
        return self.contacts
