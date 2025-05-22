class BrokenHandError(Exception):
    """Broken Hand 語言基底錯誤類別"""
    pass

class LexerError(BrokenHandError):
    """詞法分析錯誤"""
    def __init__(self, message, position=None):
        self.message = message
        self.position = position
        super().__init__(f"LexerError: {message} at {position}")

class ParserError(BrokenHandError):
    """語法分析錯誤"""
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(f"ParserError: {message} near token '{token}'")

class RuntimeError(BrokenHandError):
    """執行時錯誤"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"RuntimeError: {message}")

class NameError(RuntimeError):
    """變數或函數名稱未定義錯誤"""
    def __init__(self, name):
        message = f"Name '{name}' is not defined"
        super().__init__(message)

class TypeError(RuntimeError):
    """型別錯誤"""
    def __init__(self, expected, received):
        message = f"Type error: expected {expected}, but got {received}"
        super().__init__(message)

class ZeroDivisionError(RuntimeError):
    """除以零錯誤"""
    def __init__(self):
        message = "Division by zero"
        super().__init__(message)

class ReturnValue(Exception):
    """用於函數 return 值的特殊例外，用於控制流程"""
    def __init__(self, value):
        self.value = value
