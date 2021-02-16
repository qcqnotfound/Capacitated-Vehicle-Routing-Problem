class Node:
    def __init__(self, label, x, y, request):
        self.__label = label
        self.__x = x
        self.__y = y
        self.__request = request

    def get_label(self):
        return self.__label

    def get_request(self):
        return self.__request

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y