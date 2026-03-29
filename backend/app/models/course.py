from typing import TypedDict, NotRequired
COURSE_COLLECTION = "courses"

class CourseDocument(TypedDict):
    title: str
    description: NotRequired[str | None]