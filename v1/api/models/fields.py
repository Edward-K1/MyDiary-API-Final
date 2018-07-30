""" This file declares the fields required by the classes in models and their validation criteria"""

USER_FIELDS = ("firstname", "lastname", "username", "email", "password")
DIARY_ENTRY_FIELDS = ("user_id", "title", "content")
LOGIN_FIELDS = ("email", "password")

USER_FIELDS_REGX = (
    r"^[a-zA-Z]{2,30}$", r"^[a-zA-Z]{2,30}$", r"^\w[\w\d_]{2,30}$",
    r"(^[\w\d]+[\.\w\d_]+@[\.\w\d_]+\.[\w]{2,10}$)", r".{8,60}$"
)

DIARY_FIELDS_REGX = (r"^\d{1,30}$", r"\w.{2,100}$", r"[\s\S]{2,1000000}.$")

LOGIN_FIELDS_REGX = (r"(^[\w\d]+[\.\w\d_]+@[\.\w\d_]+\.[\w]{2,10}$)", r".{8,60}$")

DEFAULT_STR_HELP = "The {0} must be a valid string {1} characters long."

CAN_CONTAIN_DIGIT_AND_UNDERSCORE = " It can optionally contain digits and underscores."

USER_FIELDS_HELP = (DEFAULT_STR_HELP.format("firstname", "2-30"),
                    DEFAULT_STR_HELP.format("lastname", "2-30"),
                    DEFAULT_STR_HELP.format("username", "2-30") +
                    CAN_CONTAIN_DIGIT_AND_UNDERSCORE,
                    "The email must be a valid email address",
                    DEFAULT_STR_HELP.format("password", "8-60"))

DIARY_ENTRIES_HELP = (
    "The user_id must be a digit representing a valid user id.",
    DEFAULT_STR_HELP.format("title", "2-100"),
    DEFAULT_STR_HELP.format("content", "2-1,000,000")
)

LOGIN_FIELDS_HELP = ("The email is invalid", DEFAULT_STR_HELP.format("password", "8-60"))
