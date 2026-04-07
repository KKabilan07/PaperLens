from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SectionBase(BaseModel):
    section_name: str
    content: str
    page_numbers: Optional[List[int]] = None


class Section(SectionBase):
    id: str
    paper_id: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class PaperBase(BaseModel):
    title: str
    description: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class Paper(PaperBase):
    id: str
    user_id: str
    file_path: Optional[str] = None
    word_count: Optional[int] = None
    page_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class PaperWithSections(Paper):
    sections: List[Section] = []


class PaperResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    word_count: Optional[int] = None
    page_count: Optional[int] = None
    created_at: Optional[str] = None
    sections_count: int = 0


class PaperUploadResponse(BaseModel):
    success: bool
    paper_id: str
    title: str
    sections_count: int
    word_count: Optional[int] = None
    message: str
