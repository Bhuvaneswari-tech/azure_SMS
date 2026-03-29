from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class EnrollmentBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    student_id: str = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("student_id", "studentId"),
    )
    course_id: str = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("course_id", "courseId"),
    )


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    student_id: str | None = Field(default=None, validation_alias=AliasChoices("student_id", "studentId"))
    course_id: str | None = Field(default=None, validation_alias=AliasChoices("course_id", "courseId"))


class Enrollment(EnrollmentBase):
    id: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)