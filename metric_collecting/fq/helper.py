# -*- coding: utf-8 -*


def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)

    if not isExists:
        print (path+': create successfull')
        os.makedirs(path)
        return True
    else:
        print (path+': path already exist')
        return False
