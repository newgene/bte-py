# class MetaKGLoadingError(Exception):
#
#     def __init__(self, message, code=400, *args, **kwargs):
#         self.message = message
#         self.code = code
#         super(MetaKGLoadingError, self).__init__(*args)
#
#     def __str__(self):
#         return self.message


class MetaKGLoadingError(BaseException):
    pass
